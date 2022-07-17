from django.shortcuts import render
from django.views.generic import CreateView

from players.models import Player

from .models import PerformanceReport
from .forms import (
    PerformanceReportForm,
    PerformanceReportPorteroForm,
    PerformanceReportCentralForm,
    PerformanceReportLateralForm,
    PerformanceReportMediocentroForm,
    PerformanceReportMedioOfensivoForm,
    PerformanceReportExtremoForm,
    PerformanceReportDelanteroForm,
)


class CreateReport(CreateView):
    Model = PerformanceReport
    template_name = "scouting/create_report.html"
    success_url = "portero"

    def get_form_class(self):
        if self.kwargs["position"] == "portero":
            return PerformanceReportPorteroForm
        elif self.kwargs["position"] == "central":
            return PerformanceReportCentralForm
        elif self.kwargs["position"] == "lateral":
            return PerformanceReportLateralForm
        elif self.kwargs["position"] == "mediocentro":
            return PerformanceReportMediocentroForm
        elif self.kwargs["position"] == "medio_ofensivo":
            return PerformanceReportMedioOfensivoForm
        elif self.kwargs["position"] == "extremo":
            return PerformanceReportExtremoForm
        elif self.kwargs["position"] == "delantero":
            return PerformanceReportDelanteroForm
        else:
            return PerformanceReportForm
