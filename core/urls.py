from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    # User managements
    path("accounts/", include("allauth.urls")),
    # Local Apps
    path("", include("pages.urls")),
    path("external_data/", include("scrapes.urls")),
    path("players/", include("players.urls")),
    path("scouting/", include("scouting.urls")),
]
