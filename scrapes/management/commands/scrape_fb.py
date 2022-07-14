from django.core.management.base import BaseCommand
from django.utils import timezone

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

from scrapes.models import PlayerFbref, ScrapeJob


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
    help = "collect players data from fbref.com"
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
        scraped_from_x = "FBRef - Jugadores"

        # Creamos un archivo csv con el resultado del scrape

        # Borramos los datos que pueda haber sobre esa temporada previos
        ScrapeJob.objects.filter(origin="FB", season_from=season_x).delete()

        # Creamos una linea en el trabajo de scraping
        try:
            new_job = ScrapeJob.objects.create(
                scrape_job_id=scrape_job_uuid,
                created_date=scrape_init,
                mode=mode_x,
                origin="FB",
                scraped_from=scraped_from_x,
                season_from=season_x,
            )
        except:
            traceback.print_exc()
            print("Error al crear linea de scrape_job")

        try:
            df_temp = get_fbref_player_data(season_x)
        except:
            print("Error del código de web scraping")

        n_errores = 0

        print("Guardando información de los jugadores en la base de datos")
        for i in tqdm(range(len(df_temp))):
            try:
                PlayerFbref.objects.get_or_create(
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
                    fb_Sh=df_temp["Standard_Sh"][i],
                    fb_SoT=df_temp["Standard_SoT"][i],
                    fb_SoT_perc=df_temp["Standard_SoT%"][i],
                    fb_Sh_90=df_temp["Standard_Sh/90"][i],
                    fb_SoT_90=df_temp["Standard_SoT/90"][i],
                    fb_G_vs_Sh=df_temp["Standard_G/Sh"][i],
                    fb_G_vs_SoT=df_temp["Standard_G/SoT"][i],
                    fb_Dist=df_temp["Standard_Dist"][i],
                    fb_FK=df_temp["Standard_FK"][i],
                    fb_npxG_vs_Sh=df_temp["Expected_npxG/Sh"][i],
                    fb_G_minus_xG=df_temp["Expected_G-xG"][i],
                    fb_npxG_minus_xG=df_temp["Expected_np:G-xG"][i],
                    fb_passes_Cmp=df_temp["Total_Cmp"][i],
                    fb_passes_Att=df_temp["Total_Att"][i],
                    fb_passes_Cmp_perc=df_temp["Total_Cmp%"][i],
                    fb_passes_TotDist=df_temp["Total_TotDist"][i],
                    fb_passes_PrgDist=df_temp["Total_PrgDist"][i],
                    fb_passes_Short_Cmp=df_temp["Short_Cmp"][i],
                    fb_passes_Short_Att=df_temp["Short_Att"][i],
                    fb_passes_Short_Cmp_perc=df_temp["Short_Cmp%"][i],
                    fb_passes_Medium_Cmp=df_temp["Medium_Cmp"][i],
                    fb_passes_Medium_Att=df_temp["Medium_Att"][i],
                    fb_passes_Medium_Cmp_perc=df_temp["Medium_Cmp%"][i],
                    fb_passes_Long_Cmp=df_temp["Long_Cmp"][i],
                    fb_passes_Long_Att=df_temp["Long_Att"][i],
                    fb_passes_Long_Cmp_perc=df_temp["Long_Cmp%"][i],
                    fb_A_minus_xA=df_temp["A-xA"][i],
                    fb_key_passes=df_temp["KP"][i],
                    fb_last_third_passes=df_temp["1/3"][i],
                    fb_PPA=df_temp["PPA"][i],
                    fb_CrsPA=df_temp["CrsPA"][i],
                    fb_progresive_passes=df_temp["Prog"][i],
                    fb_progresive_passes_Att=df_temp["Att"][i],
                    fb_Pass_Types_Live=df_temp["Pass Types_Live"][i],
                    fb_Pass_Types_Dead=df_temp["Pass Types_Dead"][i],
                    fb_Pass_Types_FK=df_temp["Pass Types_FK"][i],
                    fb_Pass_Types_TB=df_temp["Pass Types_TB"][i],
                    fb_Pass_Types_Press=df_temp["Pass Types_Press"][i],
                    fb_Pass_Types_Sw=df_temp["Pass Types_Sw"][i],
                    fb_Pass_Types_Crs=df_temp["Pass Types_Crs"][i],
                    fb_Pass_Types_CK=df_temp["Pass Types_CK"][i],
                    fb_Corner_Kicks_In=df_temp["Corner Kicks_In"][i],
                    fb_Corner_Kicks_Out=df_temp["Corner Kicks_Out"][i],
                    fb_Corner_Kicks_Str=df_temp["Corner Kicks_Str"][i],
                    fb_Height_Ground=df_temp["Height_Ground"][i],
                    fb_Height_Low=df_temp["Height_Low"][i],
                    fb_Height_High=df_temp["Height_High"][i],
                    fb_Body_Parts_Left=df_temp["Body Parts_Left"][i],
                    fb_Body_Parts_Right=df_temp["Body Parts_Right"][i],
                    fb_Body_Parts_Head=df_temp["Body Parts_Head"][i],
                    fb_Body_Parts_TI=df_temp["Body Parts_TI"][i],
                    fb_Body_Parts_Other=df_temp["Body Parts_Other"][i],
                    fb_Outcomes_Cmp=df_temp["Outcomes_Cmp"][i],
                    fb_Outcomes_Offsides=df_temp["Outcomes_Off"][i],
                    fb_Outcomes_Out=df_temp["Outcomes_Out"][i],
                    fb_Outcomes_Int=df_temp["Outcomes_Int"][i],
                    fb_Outcomes_Blocks=df_temp["Outcomes_Blocks"][i],
                    fb_SCA_SCA=df_temp["SCA_SCA"][i],
                    fb_SCA_SCA90=df_temp["SCA_SCA90"][i],
                    fb_SCA_Types_PassLive=df_temp["SCA Types_PassLive"][i],
                    fb_SCA_Types_PassDead=df_temp["SCA Types_PassDead"][i],
                    fb_SCA_Types_Drib=df_temp["SCA Types_Drib"][i],
                    fb_SCA_Types_Sh=df_temp["SCA Types_Sh"][i],
                    fb_SCA_Types_Fld=df_temp["SCA Types_Fld"][i],
                    fb_SCA_Types_Def=df_temp["SCA Types_Def"][i],
                    fb_GCA_GCA=df_temp["GCA_GCA"][i],
                    fb_GCA_GCA90=df_temp["GCA_GCA90"][i],
                    fb_GCA_Types_PassLive=df_temp["GCA Types_PassLive"][i],
                    fb_GCA_Types_PassDead=df_temp["GCA Types_PassDead"][i],
                    fb_GCA_Types_Drib=df_temp["GCA Types_Drib"][i],
                    fb_GCA_Types_Sh=df_temp["GCA Types_Sh"][i],
                    fb_GCA_Types_Fld=df_temp["GCA Types_Fld"][i],
                    fb_GCA_Types_Def=df_temp["GCA Types_Def"][i],
                    fb_Tackles_Tkl=df_temp["Tackles_Tkl"][i],
                    fb_Tackles_TklW=df_temp["Tackles_TklW"][i],
                    fb_Tackles_Def_3rd=df_temp["Tackles_Def 3rd"][i],
                    fb_Tackles_Mid_3rd=df_temp["Tackles_Mid 3rd"][i],
                    fb_Tackles_Att_3rd=df_temp["Tackles_Att 3rd"][i],
                    fb_vs_Dribbles_Tkl=df_temp["Vs Dribbles_Tkl"][i],
                    fb_vs_Dribbles_Att=df_temp["Vs Dribbles_Att"][i],
                    fb_vs_Dribbles_Tkl_perc=df_temp["Vs Dribbles_Tkl%"][i],
                    fb_vs_Dribbles_Past=df_temp["Vs Dribbles_Past"][i],
                    fb_Pressures_Press=df_temp["Pressures_Press"][i],
                    fb_Pressures_Succ=df_temp["Pressures_Succ"][i],
                    fb_Pressures_perc=df_temp["Pressures_%"][i],
                    fb_Pressures_Def_3rd=df_temp["Pressures_Def 3rd"][i],
                    fb_Pressures_Mid_3rd=df_temp["Pressures_Mid 3rd"][i],
                    fb_Pressures_Att_3rd=df_temp["Pressures_Att 3rd"][i],
                    fb_Blocks=df_temp["Blocks_Blocks"][i],
                    fb_Blocks_Sh=df_temp["Blocks_Sh"][i],
                    fb_Blocks_ShSv=df_temp["Blocks_ShSv"][i],
                    fb_Blocks_Pass=df_temp["Blocks_Pass"][i],
                    fb_Interceptions=df_temp["Int"][i],
                    fb_Tkl_plus_Int=df_temp["Tkl+Int"][i],
                    fb_Clearances=df_temp["Clr"][i],
                    fb_Errors=df_temp["Err"][i],
                    fb_Touches=df_temp["Touches_Touches"][i],
                    fb_Touches_Def_Pen=df_temp["Touches_Def Pen"][i],
                    fb_Touches_Def_3rd=df_temp["Touches_Def 3rd"][i],
                    fb_Touches_Mid_3rd=df_temp["Touches_Mid 3rd"][i],
                    fb_Touches_Att_3rd=df_temp["Touches_Att 3rd"][i],
                    fb_Touches_Att_Pen=df_temp["Touches_Att Pen"][i],
                    fb_Touches_Live=df_temp["Touches_Live"][i],
                    fb_Dribbles_Succ=df_temp["Dribbles_Succ"][i],
                    fb_Dribbles_Att=df_temp["Dribbles_Att"][i],
                    fb_Dribbles_Succ_perc=df_temp["Dribbles_Succ%"][i],
                    fb_Dribbles_number_Pl=df_temp["Dribbles_#Pl"][i],
                    fb_Dribbles_Megs=df_temp["Dribbles_Megs"][i],
                    fb_Carries=df_temp["Carries_Carries"][i],
                    fb_Carries_TotDist=df_temp["Carries_TotDist"][i],
                    fb_Carries_PrgDist=df_temp["Carries_PrgDist"][i],
                    fb_Carries_Prog=df_temp["Carries_Prog"][i],
                    fb_Carries_last_third=df_temp["Carries_1/3"][i],
                    fb_Carries_CPA=df_temp["Carries_CPA"][i],
                    fb_Carries_Mis=df_temp["Carries_Mis"][i],
                    fb_Carries_Dis=df_temp["Carries_Dis"][i],
                    fb_Receiving_Targ=df_temp["Receiving_Targ"][i],
                    fb_Receiving_Rec=df_temp["Receiving_Rec"][i],
                    fb_Receiving_Rec_perc=df_temp["Receiving_Rec%"][i],
                    fb_Receiving_Prog=df_temp["Receiving_Prog"][i],
                    fb_Playing_Time_Mn_vs_MP=df_temp["Playing Time_Mn/MP"][i],
                    fb_Playing_Time_Min_perc=df_temp["Playing Time_Min%"][i],
                    fb_Starts_Min_vs_Start=df_temp["Starts_Mn/Start"][i],
                    fb_Starts_Compl=df_temp["Starts_Compl"][i],
                    fb_Subs_Subs=df_temp["Subs_Subs"][i],
                    fb_Subs_Mn_vs_Sub=df_temp["Subs_Mn/Sub"][i],
                    fb_Subs_unSub=df_temp["Subs_unSub"][i],
                    fb_Team_Success_PPM=df_temp["Team Success_PPM"][i],
                    fb_Team_Success_onG=df_temp["Team Success_onG"][i],
                    fb_Team_Success_onGA=df_temp["Team Success_onGA"][i],
                    fb_Team_Success_dif=df_temp["Team Success_+/-"][i],
                    fb_Team_Success_dif_90=df_temp["Team Success_+/-90"][i],
                    fb_Team_Success_On_Off=df_temp["Team Success_On-Off"][i],
                    fb_Team_Success_xG_onxG=df_temp["Team Success (xG)_onxG"][i],
                    fb_Team_Success_xG_onxGA=df_temp["Team Success (xG)_onxGA"][i],
                    fb_Team_Success_xG_xGdif=df_temp["Team Success (xG)_xG+/-"][i],
                    fb_Team_Success_xG_xGdif_90=df_temp["Team Success (xG)_xG+/-90"][i],
                    fb_Team_Success_xG_On_Off=df_temp["Team Success (xG)_On-Off"][i],
                    fb_Performance_2CrdY=df_temp["Performance_2CrdY"][i],
                    fb_Performance_Fouls=df_temp["Performance_Fls"][i],
                    fb_Performance_Fouls_drawn=df_temp["Performance_Fld"][i],
                    fb_Performance_Offsides=df_temp["Performance_Off"][i],
                    fb_Performance_Cross=df_temp["Performance_Crs"][i],
                    fb_Performance_Interceptions=df_temp["Performance_Int"][i],
                    fb_Performance_TklW=df_temp["Performance_TklW"][i],
                    fb_Performance_PKwon=df_temp["Performance_PKwon"][i],
                    fb_Performance_PKconceded=df_temp["Performance_PKcon"][i],
                    fb_Performance_OG=df_temp["Performance_OG"][i],
                    fb_Performance_Recov=df_temp["Performance_Recov"][i],
                    fb_Aerial_Duels_Won=df_temp["Aerial Duels_Won"][i],
                    fb_Aerial_Duels_Lost=df_temp["Aerial Duels_Lost"][i],
                    fb_Aerial_Duels_Won_perc=df_temp["Aerial Duels_Won%"][i],
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
