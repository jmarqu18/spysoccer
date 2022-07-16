from django.contrib import admin

from .models import Player, PlayerStats, GoalkeeperStats, Index, Scoring, ScoringRequest


class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "citizenship",
        "id_fbref",
        "id_understat",
        "id_transfermarkt",
        "id_capology",
    )
    search_fields = ["name", "id"]


class PlayerStatsAdmin(admin.ModelAdmin):
    search_fields = ["player__name", "id"]


class GoalkeeperStatsAdmin(admin.ModelAdmin):
    search_fields = ["player__name", "id"]


class IndexAdmin(admin.ModelAdmin):
    pass


class ScoringAdmin(admin.ModelAdmin):
    pass


class ScoringRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerStats, PlayerStatsAdmin)
admin.site.register(GoalkeeperStats, GoalkeeperStatsAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(Scoring, ScoringAdmin)
admin.site.register(ScoringRequest, ScoringRequestAdmin)
