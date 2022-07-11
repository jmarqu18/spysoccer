# scrapes/urls.py
from django.urls import path

from .views import ScrapesListView

urlpatterns = [
    path("", ScrapesListView.as_view(), name="scrapes_list"),
]
