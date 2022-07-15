# scrapes/views.py
from datetime import date
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from .models import (
    PlayerCapology,
    PlayerFbref,
    PlayerFbrefGK,
    PlayerTransfermarkt,
    PlayerUnderstat,
    ScrapeJob,
)
import csv


class ScrapesListView(ListView):
    model = ScrapeJob
    context_object_name = "scrapejobs_list"
    template_name = "scrapes/scrapejob_list.html"


class ScrapesDetailView(DetailView):
    model = ScrapeJob
    context_object_name = "scrapejob"
    template_name = "scrapes/scrapejob_detail.html"


def scrapejob_csv(request, pk, origin):
    today = date.today().strftime("%Y%m%d")
    filename = "{}_{}_data.csv".format(today, origin)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={}".format(filename)

    # Creamos el writer del CSV
    writer = csv.writer(response)

    # Diseñamos el modelo
    if origin == "FB":
        mod = "PlayerFbref"
        data = PlayerFbref.objects.filter(scrape_job=pk).values_list()
        colums = PlayerFbref._meta.get_fields()
    if origin == "FG":
        mod = "PlayerFbrefGK"
        data = PlayerFbrefGK.objects.filter(scrape_job=pk).values_list()
        colums = PlayerFbrefGK._meta.get_fields()
    if origin == "CA":
        mod = "PlayerCapology"
        data = PlayerCapology.objects.filter(scrape_job=pk).values_list()
        colums = PlayerCapology._meta.get_fields()
    if origin == "TM":
        mod = "PlayerTransfermarkt"
        data = PlayerTransfermarkt.objects.filter(scrape_job=pk).values_list()
        colums = PlayerTransfermarkt._meta.get_fields()
    if origin == "US":
        mod = "PlayerUnderstat"
        data = PlayerUnderstat.objects.filter(scrape_job=pk).values_list()
        colums = PlayerUnderstat._meta.get_fields()

    # Limpiamos las columnas
    cols = []
    replace_text = "scrapes.{}.".format(mod)
    for col in colums:
        cols.append(str(col).replace(replace_text, ""))

    # Añadimos el header limpio
    writer.writerow(cols)

    # Ciclo para recorrer las filas
    for row in data:
        writer.writerow(row)

    return response
