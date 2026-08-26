from django.urls import path
from .views import google_login, logout_view, me_view

urlpatterns = [
    path("google/", google_login, name="google-login"),
    path("logout/", logout_view, name="logout"),
    path("current-user/", me_view, name="current-user"),
]
