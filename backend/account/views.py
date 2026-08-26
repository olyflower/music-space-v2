from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.conf import settings


@api_view(["POST"])
def google_login(request):
    token = request.data.get("token")

    if not token:
        return Response({"error": "Token is required"}, status=400)

    try:
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        return Response({"error": "Invalid token"}, status=400)

    email = id_info["email"]
    name = id_info.get("name", "")

    user, created = User.objects.get_or_create(
        username=email, defaults={"email": email, "first_name": name}
    )

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    response = Response(
        {
            "user": {
                "email": user.email,
                "name": user.first_name,
            }
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60 * 24,
    )
    response.set_cookie(
        key="refresh_token",
        value=str(refresh),
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60 * 24 * 30,
    )

    return response


@api_view(["POST"])
def logout_view(request):
    response = Response({"message": "Logged out"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@api_view(["GET"])
def me_view(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return Response({"error": "Not authenticated"}, status=401)

    try:
        validated_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(validated_token)
    except InvalidToken:
        return Response({"error": "Invalid token"}, status=401)

    return Response(
        {
            "email": user.email,
            "name": user.first_name,
        }
    )
