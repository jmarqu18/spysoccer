from django.urls import path

from .views import CreateReport, UpdateReport, ReportList, DeleteReport


urlpatterns = [
    path("", ReportList.as_view(), name="reports_list_view"),
    path("<uuid:pk>/create_report/", CreateReport.as_view(), name="creation_report"),
    path("<uuid:pk>/update_report/", UpdateReport.as_view(), name="update_report_view"),
    path("<uuid:pk>/delete_report/", DeleteReport.as_view(), name="delete_report_view"),
]
