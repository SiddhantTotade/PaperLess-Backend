from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from rest_framework.response import Response

from django.conf import settings


class UserLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code == 200:
                access_token = response.data.get("access")
                refresh_token = response.data.get("refresh")

                response.set_cookie(
                    "access",
                    access_token,
                    max_age=settings.SIMPLE_JWT["AUTH_COOKIE_MAX_AGE"],
                    path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                response.set_cookie(
                    "refresh",
                    refresh_token,
                    max_age=settings.SIMPLE_JWT["AUTH_COOKIE_MAX_AGE"],
                    path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )

                return response
        except:
            return Response(
                {"errors": {"non_field_errors": ["Email or Password is not valid"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )