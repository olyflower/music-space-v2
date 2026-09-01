from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("player.urls")),
    path("api/auth/", include("account.urls")),
    path("api/", include("music.urls")),
]
