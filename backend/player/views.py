from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .client import search_and_parse_tracks


@api_view(["GET"])
def search_view(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return Response(
            {"error": "Query parameter q is required"},
            status=400,
        )

    cache_key = f"search:{query.lower()}"
    cached_result = cache.get(cache_key)

    if cached_result is not None:
        return Response({"results": cached_result})

    tracks = search_and_parse_tracks(query)

    cache.set(cache_key, tracks, timeout=300)

    return Response({"results": tracks})
