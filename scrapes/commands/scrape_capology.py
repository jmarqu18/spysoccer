from django.core.management.base import BaseCommand
from sys import stdout

# Base
import pandas as pd
import ScraperFC as sfc
import traceback

from scraping.models import CapologyPlayer


def get_capology_player_data(season):
    # Preparamos unas listas para recorrer las ligas (y sus nombres)
    comps = ["La Liga", "EPL", "Bundesliga", "Serie A", "Ligue 1"]

    season_x = season.split("-")[1]

    # Generamos una lista vacía para albergar los df de cada competicion
    list_dfs = []
    for i, comp in enumerate(comps):

        # generamos un nombre para este df
        nombre_df = "df_{0}_{1}".format(comp, season)

        # Web scraping from capology.com
        scraper = sfc.Capology()
        try:
            globals()[nombre_df] = scraper.scrape_salaries(
                year=season_x, league=comp, currency="eur"
            )
        except:
            traceback.print_exc()

        # Añadimos las columnas con la temporada y la competición
        globals()[nombre_df]["season"] = season
        globals()[nombre_df]["comp"] = comp

        list_dfs.append(globals()[nombre_df])

    # Unimos los df resultantes por liga
    df_capology = pd.concat(list_dfs).reset_index(drop=True)

    for i in range(len(df_capology)):
        try:
            CapologyPlayer.objects.get_or_create(
                player_name_cap=df_capology.iloc[i, 0],
                anual_gross_cap=df_capology.iloc[i, 2],
                age_cap=df_capology.iloc[i, 5],
                position_cap=df_capology.iloc[i, 4],
                country_cap=df_capology.iloc[i, 6],
                team_cap=df_capology.iloc[i, 7],
                competition_cap=df_capology.iloc[i, 8],
                season_cap=df_capology.iloc[i, 9],
            )
            print("%s added" % (df_capology.iloc[i, 0],))
        except:
            traceback.print_exc()
            print("%s already exists" % (df_capology.iloc[i, 0],))
    stdout.write("job completado")

    return df_capology


class Command(BaseCommand):
    help = "collect players data from Understat.com"
    # define logic of command

    def add_arguments(self, parser):
        parser.add_argument("season", type=str)

    def handle(self, *args, **options):
        season_x = options["season"]

        df_temp = get_capology_player_data(season_x)

        df_temp.to_csv("test.csv", decimal=",", index=False)

        self.stdout.write("Comando finalizado - JJ")
