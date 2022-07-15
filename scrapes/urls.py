# scrapes/urls.py
from django.urls import path

from .views import ScrapesListView, ScrapesDetailView, scrapejob_csv

urlpatterns = [
    path("", ScrapesListView.as_view(), name="scrapes_list"),
    path("<uuid:pk>/", ScrapesDetailView.as_view(), name="scrapes_detail"),
    path("csv/<origin>/<uuid:pk>/", scrapejob_csv, name="scrapejob_csv"),
]
