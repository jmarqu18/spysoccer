from django.urls import path

from players.views import (
    PlayersListView,
    PlayersPositionListView,
    players_csv,
    scoring_request,
    similarity_request,
)

urlpatterns = [
    path("", PlayersListView.as_view(), name="players_list"),
    path(
        "<position>/",
        PlayersPositionListView.as_view(),
        name="players_list_by_position",
    ),
    path("csv_players/", players_csv, name="players_csv"),
    path("scoring_request/", scoring_request, name="scoring_request"),
    path("similarity_request/", similarity_request, name="similarity_request"),
]
