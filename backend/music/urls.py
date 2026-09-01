from django.urls import path
from .views import add_favorite, remove_favorite, list_favorites

urlpatterns = [
    path("favorites/", list_favorites, name="list-favorites"),
    path("favorites/add/", add_favorite, name="add-favorite"),
    path("favorites/<str:spotify_id>/", remove_favorite, name="remove-favorite"),
]
