from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files import File

# Base
import pandas as pd
import json
import uuid
import lxml
from tqdm import tqdm
from cleantext import clean

import traceback

# Web Scraping
import requests
from bs4 import BeautifulSoup

from scrapes.models import PlayerUnderstat, ScrapeJob


def get_understat_player_data_by_teams(season):
    # Preparamos unas listas para recorrer las ligas (y sus nombres)
    comps = ["La_liga", "EPL", "Bundesliga", "Serie_A", "Ligue_1"]
    comps_name = ["La Liga", "Premier League", "Bundesliga", "Serie A", "Ligue 1"]

    url_base = "https://understat.com/league"

    # Definimos las variables base
    url_base_teams = "https://understat.com/team/"

    season_x = season.split("-")[0]

    # Generamos una lista vacía para albergar las url de cada competicion
    list_urls_leagues = []

    # Generamos una lista vacía para albergar los df de cada competicion
    list_dfs = []
    for i, comp in enumerate(comps):
        print("Extrayendo datos de Understat de {}.".format(comps_name[i]))

        # Construimos las Urls de las ligas
        url = "{0}/{1}/{2}".format(url_base, comp, season_x)

        # Scrapeamos buscando los nombres de los equipos de la liga en dicha temporada
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "lxml")

        # Los datos están en el script con Var TeamData
        string = soup.find_all("script")[2].string

        # Buscamos los simbolos de comienzo y fin del json
        ind_start = string.index("('") + 2
        ind_end = string.index("')")

        # Limpiamos el texto para convertirlo a json luego
        json_data = string[ind_start:ind_end]
        json_data = json_data.encode("utf8").decode("unicode_escape")

        # Convertir string a formato json
        teams_data = json.loads(json_data)

        # Recorremos el json montado para saber los nombres de los equipos
        for key in teams_data.keys():  # Equipos
            team = teams_data[key]["title"].replace(" ", "_")
            url_team = "{0}{1}/{2}".format(url_base_teams, team, season_x)

            # generamos un nombre para este df de equipo
            nombre_df = "df_{0}_{1}".format(team, season)

            # Web scraping from understat.com
            res = requests.get(url_team)
            soup = BeautifulSoup(res.content, "lxml")

            # print("Extrayendo datos de {}.".format(team))

            # Var Player data en json
            string = soup.find_all("script")[3].string

            # localizamos los inicio y fin del json
            ind_start = string.index("('") + 2
            ind_end = string.index("')")

            # Limpiamos el texto para convertirlo a json luego
            json_data = string[ind_start:ind_end]
            json_data = json_data.encode("utf8").decode("unicode_escape")

            # Convertir string a formato json
            data = json.loads(json_data)

            # creamos las listas vacias con las variables que queremos
            id_player_us = []
            player_name = []
            team = []
            key_passes = []
            xGChain = []
            xGBuildup = []
            time = []
            position = []

            # poblamos las listas que hemos preparado con los datos de cada jugador
            for player in data:
                id_player_us.append(player["id"])
                player_name.append(clean(player["player_name"], lower=False))
                team.append(clean(player["team_title"], lower=False))
                key_passes.append(int(player["key_passes"]))
                xGChain.append(float(player["xGChain"]))
                xGBuildup.append(float(player["xGBuildup"]))
                time.append(int(player["time"]))
                position.append(player["position"])

            # Creamos el dataframe
            columnas = [
                "us_id_player",
                "us_player_name",
                "us_team",
                "us_key_passes",
                "us_xGChain",
                "us_xGBuildup",
                "time",
                "us_position",
            ]
            globals()[nombre_df] = pd.DataFrame(
                [
                    id_player_us,
                    player_name,
                    team,
                    key_passes,
                    xGChain,
                    xGBuildup,
                    time,
                    position,
                ],
                index=columnas,
            ).T

            # Generamos columnas extra (por 90 min)
            globals()[nombre_df]["us_key_passes_90"] = (
                globals()[nombre_df]["us_key_passes"] / globals()[nombre_df]["time"]
            ) * 90
            globals()[nombre_df]["us_xGChain_90"] = (
                globals()[nombre_df]["us_xGChain"] / globals()[nombre_df]["time"]
            ) * 90
            globals()[nombre_df]["us_xGBuildup_90"] = (
                globals()[nombre_df]["us_xGBuildup"] / globals()[nombre_df]["time"]
            ) * 90

            # Añadimos las columnas con la temporada y la competición
            globals()[nombre_df]["us_season"] = season
            globals()[nombre_df]["us_comp"] = comps_name[i]

            list_dfs.append(globals()[nombre_df])

    # Unimos los df resultantes por equipo
    df_understat = pd.concat(list_dfs).reset_index(drop=True)

    # Ordenamos las columnas, y eliminamos "time" que no nos hace falta
    df_understat = df_understat[
        [
            "us_id_player",
            "us_player_name",
            "us_position",
            "us_team",
            "us_season",
            "us_comp",
            "us_key_passes",
            "us_xGChain",
            "us_xGBuildup",
            "us_key_passes_90",
            "us_xGChain_90",
            "us_xGBuildup_90",
        ]
    ]

    return df_understat


class Command(BaseCommand):
    help = "collect players data from Understat.com"
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
        scraped_from_x = "Understat - From Teams"

        # Creamos un archivo csv con el resultado del scrape
        # df_temp.to_csv("us_temp.csv", decimal=",", index=False)

        # with open("/us_temp.csv") as f:
        # self.license_file.save("test.csv", File(f))

        # Borramos los datos que pueda haber sobre esa temporada previos
        ScrapeJob.objects.filter(origin="US", season_from=season_x).delete()

        # Creamos una linea en el trabajo de scraping
        try:
            new_job = ScrapeJob.objects.create(
                scrape_job_id=scrape_job_uuid,
                created_date=scrape_init,
                mode=mode_x,
                origin="US",
                scraped_from=scraped_from_x,
                season_from=season_x,
            )
        except:
            traceback.print_exc()
            print("Error al crear linea de scrape_job")

        try:
            df_temp = get_understat_player_data_by_teams(season_x)
        except:
            print("Error del código de web scraping")

        n_errores = 0

        print("Guardando información de los jugadores en la base de datos")
        for i in tqdm(range(len(df_temp))):
            try:
                PlayerUnderstat.objects.get_or_create(
                    us_player_id=df_temp.iloc[i, 0],
                    us_player_name=df_temp.iloc[i, 1],
                    us_position=df_temp.iloc[i, 2],
                    us_team=df_temp.iloc[i, 3],
                    us_season=df_temp.iloc[i, 4],
                    us_comp=df_temp.iloc[i, 5],
                    us_key_passes=df_temp.iloc[i, 6],
                    us_xGChain=df_temp.iloc[i, 7],
                    us_xGBuildup=df_temp.iloc[i, 8],
                    us_key_passes_90=df_temp.iloc[i, 9],
                    us_xGChain_90=df_temp.iloc[i, 10],
                    us_xGBuildup_90=df_temp.iloc[i, 11],
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
