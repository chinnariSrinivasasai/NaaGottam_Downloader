from django.contrib import admin

from .models import DownloadHistory


@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "url",
        "quality",
        "created_at",
    )

    search_fields = (
        "url",
    )

    list_filter = (
        "quality",
        "created_at",
    )