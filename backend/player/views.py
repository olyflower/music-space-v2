from django.http import JsonResponse
from .client import search_and_parse_tracks


def search_view(request):
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse({"error": "Query parameter q is required"}, status=400)
    tracks = search_and_parse_tracks(query)
    return JsonResponse({"results": tracks})
