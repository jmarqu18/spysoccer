from django.urls import path

from .views import CreateReport


urlpatterns = [
    path("create/<position>", CreateReport.as_view(), name="creation_report")
]
