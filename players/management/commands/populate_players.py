from django.core.management.base import BaseCommand
from django.utils import timezone

import pandas as pd
from itertools import islice
import traceback
import uuid

from players.models import Player


class Command(BaseCommand):
    help = "Loads players mapping from CSV file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        start_time = timezone.now()
        player_uuid = uuid.uuid4()
        file_path = options["file_path"]
        data = pd.read_csv(file_path)
        data.info()
        # Lista para albergar todos los player objects

        # Borramos los datos que pueda haber sobre esa temporada previos
        Player.objects.all().delete()

        players = [
            Player(
                name=row["name"],
                also_named=row["also_named"],
                dob=row["dob"],
                image=row["image"],
                citizenship=row["citizenship"],
                height=row["height"],
                foot=row["foot"],
                position=row["position"],
                position_norm=row["position_norm"],
                id_fbref=row["fb_id_player"],
                id_understat=row["us_id_player"],
                id_transfermarkt=row["tm_player_id"],
                id_capology=row["cap_player_id"],
            )
            for i, row in data.iterrows()
        ]

        if players:
            Player.objects.bulk_create(players, 1000)

        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )
