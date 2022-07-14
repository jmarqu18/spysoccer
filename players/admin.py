from django.contrib import admin

from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "citizenship",
        "id_fbref",
        "id_understat",
        "id_transfermarkt",
        "id_capology",
    )


admin.site.register(Player, PlayerAdmin)
