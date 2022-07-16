from django.urls import path

from players.views import (
    PlayersListView,
    players_csv,
    scoring_request,
)

urlpatterns = [
    path("", PlayersListView.as_view(), name="players_list"),
    path("csv_players/", players_csv, name="players_csv"),
    path("scoring_request/", scoring_request, name="scoring_request"),
]
