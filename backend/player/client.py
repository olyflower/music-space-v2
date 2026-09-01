import requests
from decouple import config
from django.core.cache import cache

SPOTIFY_CLIENT_ID = config("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = config("SPOTIFY_CLIENT_SECRET")

TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"


def get_access_token():
    token = cache.get("spotify_access_token")

    if token:
        return token

    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        },
        timeout=5,
    )
    response.raise_for_status()

    data = response.json()
    token = data["access_token"]

    cache.set(
        "spotify_access_token", token, timeout=max(data.get("expires_in", 3600) - 60, 1)
    )

    return token


def search_tracks(query, limit=10):
    token = get_access_token()
    response = requests.get(
        SEARCH_URL,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "q": query,
            "type": "track",
            "limit": limit,
        },
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def parse_track(track_data):
    return {
        "spotify_id": track_data["id"],
        "title": track_data["name"],
        "artist": ", ".join(artist["name"] for artist in track_data["artists"]),
        "album": track_data["album"]["name"],
        "duration_ms": track_data["duration_ms"],
        "cover_url": (
            track_data["album"]["images"][0]["url"]
            if track_data["album"]["images"]
            else None
        ),
        "spotify_url": track_data["external_urls"]["spotify"],
    }


def search_and_parse_tracks(query, limit=10):
    raw_result = search_tracks(query, limit=limit)
    return [parse_track(track) for track in raw_result["tracks"]["items"]]
