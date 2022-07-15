from django.urls import path

from players.views import PlayersListView

urlpatterns = [
    path("", PlayersListView.as_view(), name="players_list"),
]
