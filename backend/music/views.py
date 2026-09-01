from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Track, FavoriteTrack
from .serializers import TrackSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    track_data = request.data.get("track")

    if not track_data:
        return Response(
            {"error": "Track data is required"},
            status=400,
        )

    serializer = TrackSerializer(data=track_data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    validated_data = serializer.validated_data

    track, _ = Track.objects.get_or_create(
        spotify_id=validated_data["spotify_id"],
        defaults=validated_data,
    )

    favorite, created = FavoriteTrack.objects.get_or_create(
        user=request.user,
        track=track,
    )

    if not created:
        return Response(
            {"message": "Track already in favorites"},
            status=200,
        )

    return Response(
        {"message": "Added to favorites"},
        status=201,
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_favorite(request, spotify_id):
    deleted, _ = FavoriteTrack.objects.filter(
        user=request.user, track__spotify_id=spotify_id
    ).delete()

    if not deleted:
        return Response({"error": "Not found in favorites"}, status=404)

    return Response({"message": "Removed from favorites"}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    favorites = (
        FavoriteTrack.objects.filter(user=request.user)
        .select_related("track")
        .order_by("-added_at")
    )

    tracks = [fav.track for fav in favorites]

    return Response({"results": TrackSerializer(tracks, many=True).data})
