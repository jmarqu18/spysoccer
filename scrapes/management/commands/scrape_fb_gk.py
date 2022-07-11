from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files import File

# Base
import pandas as pd
import numpy as np
import uuid
import lxml
from tqdm import tqdm
from cleantext import clean

import traceback

# Web Scraping
import requests
from bs4 import BeautifulSoup

from scrapes.models import PlayerFbrefGK, ScrapeJob


def get_fbref_player_data(season, only_gk=False):

    # Variables iniciales
    url_base = "https://fbref.com/en/comps/Big5/"

    list_urls = [
        "/stats/players/Big-5-European-Leagues-Stats#stats_standard",
        "/shooting/players/Big-5-European-Leagues-Stats#stats_shooting",
        "/passing/players/Big-5-European-Leagues-Stats#stats_passing",
        "/passing_types/players/Big-5-European-Leagues-Stats#stats_passing_types",
        "/gca/jugadores/players/Big-5-European-Leagues-Stats#stats_gca",
        "/defense/jugadores/players/Big-5-European-Leagues-Stats#stats_defense",
        "/possession/jugadores/players/Big-5-European-Leagues-Stats#stats_possession",
        "/playingtime/jugadores/players/Big-5-European-Leagues-Stats#stats_playing_time",
        "/misc/jugadores/players/Big-5-European-Leagues-Stats#stats_misc",
    ]
    list_urls_gk = [
        "/stats/players/Big-5-European-Leagues-Stats#stats_standard",
        "/keepers/players/Big-5-European-Leagues-Stats#stats_keeper",
        "/keepersadv/players/Big-5-European-Leagues-Stats#stats_keeper_adv",
    ]

    # unimos las dos listas en una lista
    urls = [list_urls, list_urls_gk]

    if only_gk == True:
        lista_urls = urls[1]
    else:
        lista_urls = urls[0]

    # Reinicializamos la variable resultante
    list_df = []
    for url in lista_urls:
        # creamos el nombre para el df
        nombre_df = "df_{0}_{1}".format(url.split("#")[1], season)
        url_complete = "{0}{1}{2}".format(url_base, season, url)

        print("Extrayendo datos de FBRef del Big5 sobre: {}".format(url.split("#")[1]))

        # Request
        r = requests.get(url_complete)
        soup = BeautifulSoup(r.content, "html.parser")

        # Usamos globals() para crear los nombres de los df de un modo dinámico
        globals()[nombre_df] = pd.read_html(
            str(
                soup.find(
                    "table",
                    class_="min_width sortable stats_table min_width shade_zero",
                )
            )
        )[0]

        # Limpieza del DF
        # generamos una lista vacia para guardar los nombres combinados de las columnas
        columnas = []
        # recorremos las columnas del df y combinamos los nombres omitiendo las columnas "Unnamed"
        for col1, col2 in globals()[nombre_df].columns:
            if str(col1).startswith("Unnamed"):
                colName = str(col2)
            else:
                colName = str(col1) + "_" + str(col2)
            columnas.append(colName)

        # cambiamos las columnas multindex por estas ya combinadas
        globals()[nombre_df].columns = columnas

        # eliminamos las columnas RL y Partidos
        globals()[nombre_df].drop(columns=["Rk", "Matches"], inplace=True)

        # limpiamos las filas que eran cabeceras inicialmente (Incluyen 'Jugador' en la columna Jugador)
        globals()[nombre_df].drop(
            globals()[nombre_df][globals()[nombre_df]["Player"] == "Player"].index,
            inplace=True,
        )

        # Añadimos los ids de FBRef de cada jugador (solo lo haremos en el primero)
        if url.split("#")[1] == "stats_standard":
            list_ids_fb_players = []
            for p in soup.find_all("td", {"data-stat": "player"}):
                list_ids_fb_players.append(p.attrs["data-append-csv"])

            globals()[nombre_df]["fb_id_player"] = list_ids_fb_players

        # Limpiamos las columnas Nation, Comp y Pos
        globals()[nombre_df]["Nation"] = globals()[nombre_df]["Nation"].apply(
            lambda x: x.split(" ")[1] if x is not np.nan else "-"
        )
        globals()[nombre_df]["Comp"] = globals()[nombre_df]["Comp"].apply(
            lambda x: x.split(" ", 1)[1]
        )
        globals()[nombre_df]["Pos"] = globals()[nombre_df]["Pos"].apply(
            lambda x: x.split(",")[0] if x is not np.nan else "-"
        )

        # Limpiamos los nombres de los jugadores (para luego poder cruzarlos mejor)
        globals()[nombre_df]["Player"] = globals()[nombre_df]["Player"].apply(
            lambda x: clean(x, lower=False)
        )

        # añadimos la temporada al df
        globals()[nombre_df]["Season"] = season
        # añadimos el df a nuestra lista de tablas
        list_df.append(globals()[nombre_df])

        # Definimos unas columnas sobre las que uniremos los dfs
        columns_to_merge = [
            "Season",
            "Player",
            "Nation",
            "Pos",
            "Squad",
            "Comp",
            "Age",
            "Born",
        ]

        # Definimos el df sobre el que iteraremos
        df_base = list_df[0].loc[:, columns_to_merge]

        # Comprobamos que no hay jugadores duplicados
        if len(df_base[df_base.duplicated()]) > 0:
            df_base.drop_duplicates()  # eliminamos duplicados por todas las columnas

        # Recorremos la lista de dfs para unirla con los demas
        for i, df in enumerate(list_df):
            df_base = df_base.merge(
                list_df[i], how="left", on=columns_to_merge, suffixes=("", "_y")
            )

        # eliminamos cualquier columna duplicada
        df_base.drop(df_base.filter(regex="_y$").columns, axis=1, inplace=True)

        # Si estamos scrapeando solo jugadores, eliminamos los porteros (GK) y viceversa
        if only_gk == True:
            df_base = df_base.loc[df_base["Pos"] == "GK"]
        else:
            df_base = df_base.loc[df_base["Pos"] != "GK"]

        df_base = df_base.fillna(0).reset_index(drop=True)

    return df_base


class Command(BaseCommand):
    help = "collect players data from Fbref.com"
    # define logic of command

    def add_arguments(self, parser):
        parser.add_argument("season", type=str)
        parser.add_argument("--manual", action="store_true")

    def handle(self, *args, **options):
        # Definimos las variables para crear la línea de scrape_job
        scrape_job_uuid = uuid.uuid4()
        season_x = options["season"]
        if options["manual"]:
            mode_x = "Manual"
        else:
            mode_x = "Automático"
        scrape_init = timezone.now()
        scraped_from_x = "FBRef - Porteros"

        # Creamos un archivo csv con el resultado del scrape

        # Borramos los datos que pueda haber sobre esa temporada previos
        ScrapeJob.objects.filter(origin="FG", season_from=season_x).delete()

        # Creamos una linea en el trabajo de scraping
        try:
            new_job = ScrapeJob.objects.create(
                scrape_job_id=scrape_job_uuid,
                created_date=scrape_init,
                mode=mode_x,
                origin="FG",
                scraped_from=scraped_from_x,
                season_from=season_x,
            )
        except:
            traceback.print_exc()
            print("Error al crear linea de scrape_job")

        try:
            df_temp = get_fbref_player_data(season_x, only_gk=True)
        except:
            print("Error del código de web scraping")

        n_errores = 0

        print("Guardando información de los jugadores en la base de datos")
        for i in tqdm(range(len(df_temp))):
            try:
                PlayerFbrefGK.objects.get_or_create(
                    fb_player_id=df_temp["fb_id_player"][i],
                    fb_player_name=df_temp["Player"][i],
                    fb_season=df_temp["Season"][i],
                    fb_nation=df_temp["Nation"][i],
                    fb_pos=df_temp["Pos"][i],
                    fb_team=df_temp["Squad"][i],
                    fb_comp=df_temp["Comp"][i],
                    fb_born=df_temp["Born"][i],
                    fb_playing_time_MP=df_temp["Playing Time_MP"][i],
                    fb_playing_time_starts=df_temp["Playing Time_Starts"][i],
                    fb_playing_time_min=df_temp["Playing Time_Min"][i],
                    fb_playing_time_90s=df_temp["Playing Time_90s"][i],
                    fb_Gls=df_temp["Performance_Gls"][i],
                    fb_Ast=df_temp["Performance_Ast"][i],
                    fb_G_minus_PK=df_temp["Performance_G-PK"][i],
                    fb_PK=df_temp["Performance_PK"][i],
                    fb_PKatt=df_temp["Performance_PKatt"][i],
                    fb_CrdY=df_temp["Performance_CrdY"][i],
                    fb_CrdR=df_temp["Performance_CrdR"][i],
                    fb_Gls_90=df_temp["Per 90 Minutes_Gls"][i],
                    fb_Ast_90=df_temp["Per 90 Minutes_Ast"][i],
                    fb_G_plus_A_90=df_temp["Per 90 Minutes_G+A"][i],
                    fb_G_plus_A_minus_PK=df_temp["Per 90 Minutes_G+A-PK"][i],
                    fb_xG=df_temp["Expected_xG"][i],
                    fb_npxG=df_temp["Expected_npxG"][i],
                    fb_xA=df_temp["Expected_xA"][i],
                    fb_npxG_plus_xA=df_temp["Expected_npxG+xA"][i],
                    fb_xG_90=df_temp["Per 90 Minutes_xG"][i],
                    fb_xA_90=df_temp["Per 90 Minutes_xA"][i],
                    fb_xG_plus_xA_90=df_temp["Per 90 Minutes_xG+xA"][i],
                    fb_npxG_90=df_temp["Per 90 Minutes_npxG"][i],
                    fb_npxG_plus_xA_90=df_temp["Per 90 Minutes_npxG+xA"][i],
                    fb_GA=df_temp["Performance_GA"][i],
                    fb_GA_90=df_temp["Performance_GA90"][i],
                    fb_SoTA=df_temp["Performance_SoTA"][i],
                    fb_saves=df_temp["Performance_Saves"][i],
                    fb_save_perc=df_temp["Performance_Save%"][i],
                    fb_W=df_temp["Performance_W"][i],
                    fb_D=df_temp["Performance_D"][i],
                    fb_L=df_temp["Performance_L"][i],
                    fb_CS=df_temp["Performance_CS"][i],
                    fb_CS_perc=df_temp["Performance_CS%"][i],
                    fb_PK_against=df_temp["Penalty Kicks_PKA"][i],
                    fb_PK_saves=df_temp["Penalty Kicks_PKsv"][i],
                    fb_PK_saves_perc=df_temp["Penalty Kicks_Save%"][i],
                    fb_PSxG=df_temp["Expected_PSxG"][i],
                    fb_PSxG_vs_SoT=df_temp["Expected_PSxG/SoT"][i],
                    fb_PSxG_dif=df_temp["Expected_PSxG+/-"][i],
                    fb_Launched_Cmp=df_temp["Launched_Cmp"][i],
                    fb_Launched_Att=df_temp["Launched_Att"][i],
                    fb_Launched_Cmp_perc=df_temp["Launched_Cmp%"][i],
                    fb_Passes_Att=df_temp["Passes_Att"][i],
                    fb_Passes_Thr=df_temp["Passes_Thr"][i],
                    fb_Passes_Launch_perc=df_temp["Passes_Launch%"][i],
                    fb_Passes_AvgLen=df_temp["Passes_AvgLen"][i],
                    fb_Goal_Kicks_Att=df_temp["Goal Kicks_Att"][i],
                    fb_Goal_Kicks_Launch_perc=df_temp["Goal Kicks_Launch%"][i],
                    fb_Goal_Kicks_AvgLen=df_temp["Goal Kicks_AvgLen"][i],
                    fb_Crosses_Opp=df_temp["Crosses_Opp"][i],
                    fb_Crosses_Stp=df_temp["Crosses_Stp"][i],
                    fb_Crosses_Stp_perc=df_temp["Crosses_Stp%"][i],
                    fb_Sweeper_OPA=df_temp["Sweeper_#OPA"][i],
                    fb_Sweeper_OPA_90=df_temp["Sweeper_#OPA/90"][i],
                    fb_Sweeper_AvgDist=df_temp["Sweeper_AvgDist"][i],
                    scrape_job=new_job,
                    created_data=timezone.now(),
                )
                # print("%s añadido" % (df_temp.iloc[i, 1],))
            except:
                traceback.print_exc()
                print("%s ya existe" % (df_temp.iloc[i, 1],))
                n_errores += 1

        # Preparamos los datos apra actualizar el estado del Job de Scraping
        if n_errores == 0:
            state_x = "OK"
        else:
            state_x = "KO"
        n_rows = len(df_temp) - n_errores
        scrape_data = {
            "number_players": n_rows,
            "number_errors": n_errores,
            "completed_date": timezone.now(),
            "state": state_x,
        }
        # Actualizamos el Job
        ScrapeJob.objects.filter(scrape_job_id=new_job.pk).update(**scrape_data)

        self.stdout.write("Job completado con {} errores".format(n_errores))
