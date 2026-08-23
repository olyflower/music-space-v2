from django.db import models


class Track(models.Model):
    spotify_id = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True)
    duration_ms = models.IntegerField()
    spotify_url = models.URLField()
    cover_url = models.URLField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist} — {self.title}"
