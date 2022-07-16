from datetime import date
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView

import csv
import pandas as pd
import uuid


from players.models import (
    GoalkeeperStats,
    Player,
    PlayerStats,
    Index,
    Scoring,
    ScoringRequest,
    Similarity,
    SimilarityRequest,
)
from players.scoring import set_scoring, filter_context_data, set_similarity
from players.forms import CalculateScoringForm, CalculateSimilarityForm


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


def scoring_request(request):
    form = CalculateScoringForm(request.POST or None)
    if request.method == "POST":

        if form.is_valid():
            # Creamos una línea de scoring request
            form = form.save(commit=False)
            # form.user = request.user
            form.id = uuid.uuid4()
            form.save()

            # Pasamos al cálulo de scoring de los jugadores
            # Definimos las ligas sobre las que haremos el cálculo
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
            positions = [
                "Central",
                "Lateral",
                "Mediocentro",
                "Medio Ofensivo",
                "Extremo",
                "Delantero",
            ]

            # La primera aproximación será hacer el cálculo de scoring por liga y posición agrupada

            # Nos traemos los datos del Index seleccionado
            index_x = form.index_used
            index = Index.objects.get(index_name=index_x)
            index_data = index.index_data
            metricas = list(index_data.keys())
            pesos = list(index_data.values())
            index_position = index.position_norm
            minutes_x = form.minutes_played_min
            new_sreq = ScoringRequest.objects.get(id=form.id)

            # Nos traemos los datos de jugadores y porteros como dataframes
            if index_position == "Portero":
                data = pd.DataFrame.from_dict(GoalkeeperStats.objects.values())
            else:
                data = pd.DataFrame.from_dict(
                    PlayerStats.objects.filter(
                        player__in=Player.objects.filter(position_norm=index_position)
                    ).values()
                )  # TODO Filtrar por temporadas en la vista

            # comenzamos a realizar los filtrados por Competición y Posición
            data_filtered = filter_context_data(data, minutes_x)

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

            return redirect("players_list")

    return render(request, "players/calculate_scoring.html", {"form": form})


def similarity_request(request):
    form = CalculateSimilarityForm(request.POST or None)
    if request.method == "POST":

        if form.is_valid():
            # Creamos una línea de scoring request
            form = form.save(commit=False)
            form.id = uuid.uuid4()
            form.save()

            # La primera aproximación será hacer el cálculo de similitud por posición agrupada

            # Nos traemos los datos del Index seleccionado
            index_x = form.index_used
            index = Index.objects.get(index_name=index_x)
            index_data = index.index_data
            metricas = list(index_data.keys())
            index_position = index.position_norm
            minutes_x = form.minutes_played_min
            new_sreq = SimilarityRequest.objects.get(id=form.id)

            # Nos traemos los datos de jugadores y porteros como dataframes
            if index_position == "Portero":
                data = pd.DataFrame.from_dict(GoalkeeperStats.objects.values())
            else:
                data = pd.DataFrame.from_dict(
                    PlayerStats.objects.filter(
                        player__in=Player.objects.filter(position_norm=index_position)
                    ).values()
                )  # TODO Filtrar por temporadas en la vista

            # comenzamos a realizar los filtrados por Competición y Posición
            data_filtered = filter_context_data(data, minutes_x)

            data_similarity = set_similarity(data_filtered, metricas)

            data_similarity_create = [
                Similarity(
                    player=Player.objects.get(id=row["player_id"]),
                    similar_player=Player.objects.get(id=row["similar_player_id"]),
                    similarity=row["similarity"],
                    similarity_request=new_sreq,
                )
                for i, row in data_similarity.iterrows()
            ]

            if data_similarity_create:
                Similarity.objects.bulk_create(data_similarity_create, 1000)

            return redirect("players_list")

    return render(request, "players/calculate_similarity.html", {"form": form})
