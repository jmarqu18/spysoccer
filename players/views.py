from django.shortcuts import render
from django.views.generic import ListView, DetailView

from players.models import Player


class PlayersListView(ListView):
    model = Player
    context_object_name = "players_list"
    template_name = "players/players_list.html"
