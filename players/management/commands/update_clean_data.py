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

from scrapes.models import PlayerFbref, ScrapeJob
from players.models import Player, PlayerStats, GoalkeeperStats


class Command(BaseCommand):
    help = "Comprueba si los datos extraidos son los más actuales y los copia en la BBDD si no."
    # define logic of command

    # def add_arguments(self, parser):
    #     parser.add_argument("season", type=str)

    def handle(self, *args, **options):
        # Definimos las variables para crear la línea de scrape_job

        # Traemos los datos de Player como "mapeo"
        queryset = Player.objects.values_list(
            "id", "id_fbref", "id_understat", "id_transfermarkt", "id_capology"
        )
        players_mapping = pd.DataFrame(
            list(queryset),
            columns=[
                "id",
                "id_fbref",
                "id_understat",
                "id_transfermarkt",
                "id_capology",
            ],
        )

        players_mapping.to_csv("./test.csv", index=False)

        queryset2 = PlayerFbref.objects.values_list()
        qs_cols = PlayerFbref._meta.get_fields()
        data = pd.DataFrame(list(queryset2), columns=qs_cols)

        data.to_csv("./test2.csv", index=False)
