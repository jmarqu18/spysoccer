from django.contrib import admin
from .models import (
    ScrapeJob,
    PlayerUnderstat,
    PlayerFbrefGK,
    PlayerFbref,
    PlayerCapology,
    PlayerTransfermarkt,
)


class ScrapeJobAdmin(admin.ModelAdmin):
    list_display = ("scraped_from", "completed_date", "state", "number_errors")


class PlayerUnderstatAdmin(admin.ModelAdmin):
    pass


class PlayerFbrefGKAdmin(admin.ModelAdmin):
    pass


class PlayerFbrefAdmin(admin.ModelAdmin):
    pass


class PlayerCapologyAdmin(admin.ModelAdmin):
    pass


class PlayerTransfermarktAdmin(admin.ModelAdmin):
    pass


admin.site.register(ScrapeJob, ScrapeJobAdmin)
admin.site.register(PlayerUnderstat, PlayerUnderstatAdmin)
admin.site.register(PlayerFbrefGK, PlayerFbrefGKAdmin)
admin.site.register(PlayerFbref, PlayerFbrefAdmin)
admin.site.register(PlayerCapology, PlayerCapologyAdmin)
admin.site.register(PlayerTransfermarkt, PlayerTransfermarktAdmin)
