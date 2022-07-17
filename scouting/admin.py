from django.contrib import admin

from .models import PerformanceReport


class PerformanceReportAdmin(admin.ModelAdmin):
    pass


admin.site.register(PerformanceReport, PerformanceReportAdmin)
