from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

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
    model = PerformanceReport
    template_name = "scouting/create_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["player_pk"] = self.kwargs["pk"]
        context["player"] = Player.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        form.instance.scout = self.request.user
        form.instance.player = Player.objects.get(pk=self.kwargs["pk"])
        # print(form.instance.job)
        # print(form.instance.technician)
        context = {
            "player_pk": self.kwargs["pk"],
            "player": Player.objects.get(pk=self.kwargs["pk"]),
        }
        return super().form_valid(form)

    def get_form_class(self):
        player_x = Player.objects.get(pk=self.kwargs["pk"])
        if player_x.position_norm == "Portero":
            return PerformanceReportPorteroForm
        elif player_x.position_norm == "Central":
            return PerformanceReportCentralForm
        elif player_x.position_norm == "Lateral":
            return PerformanceReportLateralForm
        elif player_x.position_norm == "Mediocentro":
            return PerformanceReportMediocentroForm
        elif player_x.position_norm == "Medio Ofensivo":
            return PerformanceReportMedioOfensivoForm
        elif player_x.position_norm == "Extremo":
            return PerformanceReportExtremoForm
        elif player_x.position_norm == "Delantero":
            return PerformanceReportDelanteroForm
        else:
            return PerformanceReportForm

    def get_success_url(self):
        return reverse("reports_list_view")


class ReportList(ListView):
    model = PerformanceReport
    context_object_name = "reports_list"
    template_name = "scouting/reports_list.html"


class UpdateReport(UpdateView):
    model = PerformanceReport
    template_name = "scouting/update_report.html"

    def get_queryset(self, **kwargs):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_pk"] = self.kwargs["pk"]
        context["player"] = Player.objects.get(
            pk=PerformanceReport.objects.get(pk=self.kwargs["pk"]).player.pk
        )
        return context

    def get_form_class(self):
        player_x = Player.objects.get(
            pk=PerformanceReport.objects.get(pk=self.kwargs["pk"]).player.pk
        )
        if player_x.position_norm == "Portero":
            return PerformanceReportPorteroForm
        elif player_x.position_norm == "Central":
            return PerformanceReportCentralForm
        elif player_x.position_norm == "Lateral":
            return PerformanceReportLateralForm
        elif player_x.position_norm == "Mediocentro":
            return PerformanceReportMediocentroForm
        elif player_x.position_norm == "Medio Ofensivo":
            return PerformanceReportMedioOfensivoForm
        elif player_x.position_norm == "Extremo":
            return PerformanceReportExtremoForm
        elif player_x.position_norm == "Delantero":
            return PerformanceReportDelanteroForm
        else:
            return PerformanceReportForm

    def get_success_url(self):
        return reverse("reports_list_view")


class DeleteReport(DeleteView):
    model = PerformanceReport
    template_name = "scouting/report_delete_confirm.html"

    def get_success_url(self):
        return reverse("reports_list_view")
