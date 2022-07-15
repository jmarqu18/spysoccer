from datetime import date
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

import csv

from players.models import Player


class PlayersListView(ListView):
    model = Player
    context_object_name = "players_list"
    template_name = "players/players_list.html"


def players_csv(request):
    today = date.today().strftime("%Y%m%d")
    filename = "{}_players.csv".format(today)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={}".format(filename)

    # Creamos el writer del CSV
    writer = csv.writer(response)

    data = Player.objects.values_list()
    colums = Player._meta.get_fields()

    # Limpiamos las columnas
    cols = []
    replace_text = "players.Player."
    for col in colums:
        cols.append(str(col).replace(replace_text, ""))
    cols = cols[4:]

    # Añadimos el header limpio
    writer.writerow(cols)

    # Ciclo para recorrer las filas
    for row in data:
        writer.writerow(row)

    return response
