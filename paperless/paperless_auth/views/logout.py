from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from ..serializers import logout


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh")
            serializer = logout.LogoutSerializer(
                data={"refresh": refresh_token})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response = Response(status=status.HTTP_204_NO_CONTENT)

            response.set_cookie(
                "access",
                None,
                max_age=settings.SIMPLE_JWT["AUTH_COOKIE_MAX_AGE"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )

            response.set_cookie(
                "refresh",
                None,
                max_age=settings.SIMPLE_JWT["AUTH_COOKIE_MAX_AGE"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )

            return response
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )