# scrapes/urls.py
from django.urls import path

from .views import ScrapesListView, ScrapesDetailView

urlpatterns = [
    path("", ScrapesListView.as_view(), name="scrapes_list"),
    path("<uuid:pk>/", ScrapesDetailView.as_view(), name="scrapes_detail"),
]
