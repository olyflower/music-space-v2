from rest_framework import serializers
from .models import Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            "spotify_id",
            "title",
            "artist",
            "album",
            "duration_ms",
            "cover_url",
            "spotify_url",
        ]
