from django.urls import path

from players.views import (
    PlayersListView,
    PlayersPositionListView,
    ScoringRequestList,
    SimilarityRequestList,
    ScoringList,
    SimilarityList,
    players_csv,
    scoring_request,
    similarity_request,
)

urlpatterns = [
    path("", PlayersListView.as_view(), name="players_list"),
    path("csv_players/", players_csv, name="players_csv"),
    path("scoring_request/", ScoringRequestList.as_view(), name="scoring_request_list"),
    path("scoring_request/<uuid:pk>/", ScoringList.as_view(), name="scoring_list"),
    path(
        "similarity_request/",
        SimilarityRequestList.as_view(),
        name="similarity_request_list",
    ),
    path(
        "similarity_request/<uuid:pk>/",
        SimilarityList.as_view(),
        name="similarity_list",
    ),
    path("scoring_request/create/", scoring_request, name="scoring_request"),
    path("similarity_request/create/", similarity_request, name="similarity_request"),
    path(
        "<position>/",
        PlayersPositionListView.as_view(),
        name="players_list_by_position",
    ),
]
