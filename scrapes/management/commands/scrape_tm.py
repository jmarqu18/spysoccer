from django.core.management.base import BaseCommand
from django.utils import timezone

# Base
import pandas as pd
import numpy as np
import uuid
import lxml
from tqdm import tqdm
from cleantext import clean
from datetime import datetime
import traceback

# Web Scraping
import requests
from bs4 import BeautifulSoup

from scrapes.models import PlayerTransfermarkt, ScrapeJob

pd.set_option("display.max_colwidth", 255)


def get_tm_player_data_by_teams(season):
    # Definimos las variables iniciales para construir la url en el ciclo for
    url_base = "https://www.transfermarkt.com"
    constructor_url_comp = ["/startseite/wettbewerb/", "/plus/?saison_id="]
    urls = {
        "La Liga": ["/laliga", "ES1"],
        "Premier League": ["/premier-league", "GB1"],
        "Bundesliga": ["/1-bundesliga", "L1"],
        "Serie A": ["/serie-a", "IT1"],
        "Ligue 1": ["/ligue-1", "FR1"],
    }

    # La temporada en TM se coge solo el primer año
    season = season.split("-")[0]

    # Definimos unos headers adecuados para TM
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0"
    }

    # Preparamos una lista vacia para guardar los df de los equipos
    list_dfs = []

    for comp in urls:

        print("Extrayendo datos de Transfermarkt de {}".format(comp))

        # Definimos una lista donde guardaremos las url de los equipos por campeonato
        urls_teams = []

        url = "{}{}{}{}{}{}".format(
            url_base,
            urls[comp][0],
            constructor_url_comp[0],
            urls[comp][1],
            constructor_url_comp[1],
            season,
        )
        # Web scraping
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        # Recorremos los enlaces de los equipos
        for i, url in enumerate(soup.select(".hauptlink.no-border-links a")):
            if (
                url.get("href").find("startseite/verein") > 0
            ):  # ese texto forma parte de las url de los equipos con sus jugadores
                url_temp = url.get("href")
                # Eliminamos la temporada que por defecto coge la última y queremos la solicitada
                url_temp = url_temp[:-4] + season
                # Generamos la Url completa del equipo con la tabla detallada
                url_temp = "{}{}{}".format(
                    url_base, url_temp.replace("startseite", "kader"), "/plus/1"
                )
                urls_teams.append(url_temp)

        urls_teams = list(set(urls_teams))

        for i, url_t in enumerate(urls_teams):
            # Listas vacias para los Datos de los jugadores
            list_tm_player_name = []
            list_tm_player_image = []
            list_tm_current_value = []
            list_tm_birthdate = []
            list_tm_yearbirthdate = []
            list_tm_height = []
            list_tm_citizenship = []
            list_tm_position = []
            list_tm_foot = []
            list_tm_current_club = []
            list_tm_date_joined = []
            list_tm_contract_expires = []
            list_tm_id_player = []

            # print(url_t)
            # generamos un nombre para este df
            nombre_df = "df_{0}_{1}".format(i, season)

            # Web Scraping
            r = requests.get(url_t, headers=headers)
            soup = BeautifulSoup(r.text, "lxml")

            # Seleccionamos la tabla con los datos de los jugadores
            players_rows = soup.find_all("tr", class_=["odd", "even"])

            for player in players_rows:

                # Imagen Jugador
                try:
                    tm_player_image = player.select("img.bilderrahmen-fixed")[0].get(
                        "data-src"
                    )[:-5]
                    list_tm_player_image.append(tm_player_image)
                except:
                    tm_player_image = np.nan
                    list_tm_player_image.append(tm_player_image)

                # Id Jugador
                try:
                    if len(player.select("a")) > 3:
                        tm_id_player = player.select("a")[2].get("href").split("/")[-1]
                    else:
                        tm_id_player = player.select("a")[0].get("href").split("/")[-1]
                    list_tm_id_player.append(tm_id_player)
                except:
                    tm_id_player = np.nan
                    list_tm_id_player.append(tm_id_player)

                # Nombre del jugador
                try:
                    if len(player.select("a")) > 3:
                        tm_player_name = clean(player.select("a")[2].text, lower=False)
                    else:
                        tm_player_name = clean(player.select("a")[0].text, lower=False)
                    list_tm_player_name.append(tm_player_name)
                except:
                    tm_player_name = np.nan
                    list_tm_player_name.append(tm_player_name)

                # Valor de mercado del jugador (3 campos)
                try:
                    tm_current_value = clean(
                        player.select("td.rechts.hauptlink")[0].text
                    )
                    if tm_current_value.endswith("th."):
                        tm_current_value = float(tm_current_value[3:-3]) * 1000
                    elif tm_current_value.endswith("m"):
                        tm_current_value = float(tm_current_value[3:-1]) * 1000000
                    else:
                        tm_current_value = float(tm_current_value[3:])
                    list_tm_current_value.append(tm_current_value)
                except:
                    tm_current_value = 0
                    list_tm_current_value.append(tm_current_value)

                # Posicion
                try:
                    tm_position = clean(
                        player.select(".inline-table")[0].select("td")[-1].text,
                        lower=False,
                    )
                    list_tm_position.append(tm_position)
                except:
                    tm_position = np.nan
                    list_tm_position.append(tm_position)

                # Fecha nacimiento
                try:
                    tm_birthdate = datetime.strptime(
                        (player.select(".zentriert")[1].text).split("(")[0], "%b %d, %Y"
                    )
                    # Año nacimiento
                    tm_yearbirthdate = tm_birthdate.year

                    list_tm_birthdate.append(tm_birthdate)
                    list_tm_yearbirthdate.append(tm_yearbirthdate)
                except:
                    tm_birthdate = datetime.strptime("1900-01-01", "%Y-%m-%d")
                    tm_yearbirthdate = np.nan
                    list_tm_birthdate.append(tm_birthdate)
                    list_tm_yearbirthdate.append(tm_yearbirthdate)

                # Nacionalidad
                try:
                    tm_citizenship = (
                        player.select(".zentriert")[2].select("img")[0].get("title")
                    )
                    list_tm_citizenship.append(tm_citizenship)
                except:
                    tm_citizenship = np.nan
                    list_tm_citizenship.append(tm_citizenship)

                # Equipo Actual
                try:
                    tm_current_club = (
                        player.select(".zentriert")[3].select("img")[0].get("title")
                    )
                    list_tm_current_club.append(tm_current_club)
                except:
                    tm_current_club = np.nan
                    list_tm_current_club.append(tm_current_club)

                # Pie
                try:
                    tm_foot = player.select(".zentriert")[5].text.capitalize()
                    list_tm_foot.append(tm_foot)
                except:
                    tm_foot = np.nan
                    list_tm_foot.append(tm_foot)

                # Altura
                try:
                    tm_height = clean(player.select(".zentriert")[4].text)
                    list_tm_height.append(tm_height)
                except:
                    tm_height = np.nan
                    list_tm_height.append(tm_height)

                # Fecha inicio contrato
                try:
                    tm_date_joined = datetime.strptime(
                        player.select(".zentriert")[6].text, "%b %d, %Y"
                    )
                    list_tm_date_joined.append(tm_date_joined)
                except:
                    tm_date_joined = datetime.strptime("1900-01-01", "%Y-%m-%d")
                    list_tm_date_joined.append(tm_date_joined)

                # Fecha fin contrato
                try:
                    tm_contract_expires = datetime.strptime(
                        player.select(".zentriert")[8].text, "%b %d, %Y"
                    )
                    list_tm_contract_expires.append(tm_contract_expires)
                except:
                    tm_contract_expires = datetime.strptime("1900-01-01", "%Y-%m-%d")
                    list_tm_contract_expires.append(tm_contract_expires)

            # Generamos el df del equipo
            globals()[nombre_df] = pd.DataFrame(
                [
                    list_tm_id_player,
                    list_tm_player_name,
                    list_tm_player_image,
                    list_tm_current_value,
                    list_tm_birthdate,
                    list_tm_yearbirthdate,
                    list_tm_citizenship,
                    list_tm_position,
                    list_tm_height,
                    list_tm_foot,
                    list_tm_current_club,
                    list_tm_date_joined,
                    list_tm_contract_expires,
                ],
                index=[
                    "tm_player_id",
                    "tm_player_name",
                    "tm_player_image",
                    "tm_current_value",
                    "tm_birthdate",
                    "tm_yearbirthdate",
                    "tm_citizenship",
                    "tm_position",
                    "tm_height",
                    "tm_foot",
                    "tm_current_club",
                    "tm_date_joined",
                    "tm_contract_expires",
                ],
            ).T

            globals()[nombre_df]["tm_comp"] = comp

            # Agregamos el df del equipo a la lista de los equipos
            list_dfs.append(globals()[nombre_df])

    # Unimos los df resultantes por liga
    df_transfermarkt = pd.concat(list_dfs).reset_index(drop=True).drop_duplicates()

    return df_transfermarkt


class Command(BaseCommand):
    help = "collect players data from Transfermarkt.com"
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
        scraped_from_x = "Transfermarkt - From Teams"

        # Creamos un archivo csv con el resultado del scrape

        # Borramos los datos que pueda haber sobre esa temporada previos
        ScrapeJob.objects.filter(origin="TM", season_from=season_x).delete()

        # Creamos una linea en el trabajo de scraping
        try:
            new_job = ScrapeJob.objects.create(
                scrape_job_id=scrape_job_uuid,
                created_date=scrape_init,
                mode=mode_x,
                origin="TM",
                scraped_from=scraped_from_x,
                season_from=season_x,
            )
        except:
            traceback.print_exc()
            print("Error al crear linea de scrape_job")

        try:
            df_temp = get_tm_player_data_by_teams(season_x)
            df_temp.to_csv("./test.csv", decimal=",", index=False)
        except:
            traceback.print_exc()
            print("Error del código de web scraping.")

        n_errores = 0

        print("Guardando información de los jugadores en la base de datos")
        for i in tqdm(range(len(df_temp))):
            try:
                PlayerTransfermarkt.objects.get_or_create(
                    tm_player_id=df_temp.iloc[i, 0],
                    tm_player_name=df_temp.iloc[i, 1],
                    tm_player_image_url=df_temp.iloc[i, 2],
                    tm_current_value=df_temp.iloc[i, 3],
                    tm_birthdate=df_temp.iloc[i, 4],
                    tm_yearbirthdate=df_temp.iloc[i, 5],
                    tm_citizenship=df_temp.iloc[i, 6],
                    tm_position=df_temp.iloc[i, 7],
                    tm_height=df_temp.iloc[i, 8],
                    tm_foot=df_temp.iloc[i, 9],
                    tm_current_club=df_temp.iloc[i, 10],
                    tm_date_joined=df_temp.iloc[i, 11],
                    tm_contract_expires=df_temp.iloc[i, 12],
                    tm_comp=df_temp.iloc[i, 13],
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
