import traceback
import uuid
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from sklearn.preprocessing import MinMaxScaler
import scipy.stats as ss

import pandas as pd

from players.models import (
    GoalkeeperStats,
    Index,
    Player,
    PlayerStats,
    Scoring,
    ScoringRequest,
)
from players.scoring import filter_context_data, set_scoring


class Command(BaseCommand):
    help = "Calculate Scoring de los jugadores por posición y Liga"

    def add_arguments(self, parser):
        parser.add_argument("index_code", type=str)
        parser.add_argument("season", type=str)
        parser.add_argument("minutes", type=int)

    def handle(self, *args, **options):
        start_time = timezone.now()
        index_code = options["index_code"]
        index_x = Index.objects.get(index_name=index_code)
        season = options["season"]
        minutes = options["minutes"]
        scoring_request_id = uuid.uuid4()

        # Intentamos crear la línea de Scoring Request
        try:
            new_sreq = ScoringRequest.objects.create(
                id=scoring_request_id,
                index_used=index_x,
                minutes_played_min=minutes,
                season_request=season,
            )
        except:
            traceback.print_exc()
            print("Error al crear linea de scrape_job")

        # Ahora que tenemos la linea de Request lista, vamos a por los datos
        competitions = [
            "La Liga",
            "Premier League",
            "Bundesliga",
            "Serie A",
            "Ligue 1",
        ]
        neg_metrics = [
            "goals_against",
            "goals_against_90",
            "offsides",
            "red_cards",
            "yellow_cards",
            "double_yellow_cards",
        ]

        # Nos traemos los datos de jugadores y porteros como dataframes
        if index_x.position_norm == "Portero":
            data = pd.DataFrame.from_dict(GoalkeeperStats.objects.values())
        else:
            data = pd.DataFrame.from_dict(
                PlayerStats.objects.filter(
                    player__in=Player.objects.filter(
                        position_norm=index_x.position_norm
                    )
                ).values()
            )  # TODO Filtrar por temporadas en la vista

        # comenzamos a realizar los filtrados por Competición y Posición
        data_filtered = filter_context_data(data, minutes)

        metricas = list(index_x.index_data.keys())
        pesos = list(index_x.index_data.values())

        data_scoring = set_scoring(data_filtered, metricas, pesos)

        data_scoring_create = [
            Scoring(
                player=Player.objects.get(id=row["player_id"]),
                scoring=row["scoring"],
                rank_in_context=row["rank"],
                scoring_request=new_sreq,
            )
            for i, row in data_scoring.iterrows()
        ]

        if data_scoring_create:
            Scoring.objects.bulk_create(data_scoring_create, 1000)

        self.stdout.write("Job completado sin errores")
