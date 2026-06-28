from django.db import models


class DownloadHistory(models.Model):

    QUALITY_CHOICES = [
        ("best", "Best Quality"),
        ("1080", "1080p"),
        ("720", "720p"),
        ("480", "480p"),
        ("audio", "Audio Only"),
    ]

    url = models.URLField()

    quality = models.CharField(
        max_length=20,
        choices=QUALITY_CHOICES,
    )

    download_thumbnail = models.BooleanField(
        default=False,
    )

    download_subtitle = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.url