# scrapes/views.py
from django.views.generic import ListView

from .models import ScrapeJob


class ScrapesListView(ListView):
    model = ScrapeJob
    template_name = "scrapes/scrapes_list.html"
