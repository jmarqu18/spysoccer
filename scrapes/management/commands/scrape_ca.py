from django.core.management.base import BaseCommand
from django.utils import timezone


# Base
import pandas as pd
import uuid
import lxml
from tqdm import tqdm
from cleantext import clean
from datetime import datetime

import traceback

# Web Scraping
import requests
from bs4 import BeautifulSoup

from scrapes.models import PlayerCapology, ScrapeJob


def get_capology_players(season):

    urls = {
        "Premier League": "https://www.capology.com/uk/premier-league/salaries/",
        "Serie A": "https://www.capology.com/it/serie-a/salaries/",
        "La Liga": "https://www.capology.com/es/la-liga/salaries/",
        "Bundesliga": "https://www.capology.com/de/1-bundesliga/salaries/",
        "Ligue 1": "https://www.capology.com/fr/ligue-1/salaries/",
    }

    # Generamos una lista vacía para albergar los df de cada competicion
    list_dfs = []
    try:
        for key in urls:

            print("Extrayendo los datos de Capology de {}".format(key))

            # generamos un nombre para este df
            nombre_df = "df_{0}_{1}".format(key, season)

            r = requests.get(urls[key])
            soup = BeautifulSoup(r.text, "lxml")

            data_to_clean = soup.find_all("script")[14].string
            ind_start = data_to_clean.index("[{") + 4
            ind_end = data_to_clean.index("},];")

            data_to_clean = data_to_clean[ind_start:ind_end]
            data_to_clean = data_to_clean.split("\n")

            names = []
            annual_gross_eur = []
            expiration = []
            country = []
            club = []
            ids = []

            for row in data_to_clean:
                if row.find("'name'") >= 0:
                    a = row.split(":")[1]
                    names_i = clean(a.split(">")[2].split("</a")[0], lower=False)
                    names.append(names_i)
                if row.find("'annual_gross_eur'") >= 0:
                    a = row.split(":")[1]
                    salary_i = int(a.split('"')[1])
                    annual_gross_eur.append(salary_i)
                if row.find("'expiration'") >= 0:
                    a = row.split(":")[1]
                    expiration_i = datetime.strptime(a.split('"')[1], "%Y-%m-%d")
                    expiration.append(expiration_i)
                if row.find("'country'") >= 0:
                    a = row.split(":")[1]
                    country_i = clean(a.split('"')[1], lower=False)
                    country.append(country_i)
                if row.find("'club'") >= 0:
                    a = row.split(":")[1]
                    club_i = clean(a.split(">")[1].split("</a")[0], lower=False)
                    club.append(club_i)
                if row.find("'name'") >= 0:
                    a = row.split(":")[1]
                    ids_i = BeautifulSoup(a, "lxml").find("a").get("href").split("/")[2]
                    ids.append(ids_i)

            globals()[nombre_df] = pd.DataFrame(
                [ids, names, annual_gross_eur, expiration, country, club],
                index=[
                    "cap_player_id",
                    "cap_player_name",
                    "cap_salary",
                    "cap_expiration",
                    "cap_country",
                    "cap_club",
                ],
            ).T

            # Añadimos las columnas con la temporada y la competición
            globals()[nombre_df]["cap_season"] = season
            globals()[nombre_df]["cap_comp"] = key

            list_dfs.append(globals()[nombre_df])
    except IndexError:
        print(
            "Error de índice no existente. La web de Capology debe estar fallando. Intentalo más tarde."
        )
        error = True

    # Unimos los df resultantes por liga
    df_capology = pd.concat(list_dfs).reset_index(drop=True)

    return df_capology


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
        scraped_from_x = "Capology Salaries"

        # Creamos un archivo csv con el resultado del scrape

        # Borramos los datos que pueda haber sobre esa temporada previos
        ScrapeJob.objects.filter(origin="CA", season_from=season_x).delete()

        # Creamos una linea en el trabajo de scraping
        try:
            new_job = ScrapeJob.objects.create(
                scrape_job_id=scrape_job_uuid,
                created_date=scrape_init,
                mode=mode_x,
                origin="CA",
                scraped_from=scraped_from_x,
                season_from=season_x,
            )
        except:
            traceback.print_exc()
            print("Error al crear linea de scrape_job")

        try:
            df_temp = get_capology_players(season_x)
        except:
            traceback.print_exc()
            ScrapeJob.objects.filter(origin="CA", season_from=season_x).delete()
            print("Error del código de web scraping")

        n_errores = 0

        print("Guardando información de los jugadores en la base de datos")
        for i in tqdm(range(len(df_temp))):
            try:
                PlayerCapology.objects.get_or_create(
                    ca_player_id=df_temp.iloc[i, 0],
                    ca_player_name=df_temp.iloc[i, 1],
                    ca_salary=df_temp.iloc[i, 2],
                    ca_expiration=df_temp.iloc[i, 3],
                    ca_country=df_temp.iloc[i, 4],
                    ca_team=df_temp.iloc[i, 5],
                    ca_season=df_temp.iloc[i, 6],
                    ca_comp=df_temp.iloc[i, 7],
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
        scrape_data = {
            "number_errors": n_errores,
            "completed_date": timezone.now(),
            "state": state_x,
        }
        # Actualizamos el Job
        ScrapeJob.objects.filter(scrape_job_id=new_job.pk).update(**scrape_data)

        self.stdout.write("Job completado con {} errores".format(n_errores))
