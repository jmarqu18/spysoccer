from django.urls import path

from players.views import PlayersListView, players_csv

urlpatterns = [
    path("", PlayersListView.as_view(), name="players_list"),
    path("csv_players/", players_csv, name="players_csv"),
]
