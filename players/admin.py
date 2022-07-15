from django.contrib import admin

from .models import Player, PlayerStats, GoalkeeperStats


class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "citizenship",
        "id_fbref",
        "id_understat",
        "id_transfermarkt",
        "id_capology",
    )


class PlayerStatsAdmin(admin.ModelAdmin):
    pass


class GoalkeeperStatsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerStats, PlayerStatsAdmin)
admin.site.register(GoalkeeperStats, GoalkeeperStatsAdmin)
