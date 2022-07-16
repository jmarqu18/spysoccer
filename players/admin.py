from django.contrib import admin

from .models import (
    Player,
    PlayerStats,
    GoalkeeperStats,
    Index,
    Scoring,
    ScoringRequest,
    Similarity,
    SimilarityRequest,
)


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


class SimilarityAdmin(admin.ModelAdmin):
    pass


class SimilarityRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerStats, PlayerStatsAdmin)
admin.site.register(GoalkeeperStats, GoalkeeperStatsAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(Scoring, ScoringAdmin)
admin.site.register(ScoringRequest, ScoringRequestAdmin)
admin.site.register(Similarity, SimilarityAdmin)
admin.site.register(SimilarityRequest, SimilarityRequestAdmin)
