# scrapes/views.py
from django.views.generic import ListView, DetailView

from .models import ScrapeJob


class ScrapesListView(ListView):
    model = ScrapeJob
    context_object_name = "scrapejobs_list"
    template_name = "scrapes/scrapejob_list.html"


class ScrapesDetailView(DetailView):
    model = ScrapeJob
    context_object_name = "scrapejob"
    template_name = "scrapes/scrapejob_detail.html"
