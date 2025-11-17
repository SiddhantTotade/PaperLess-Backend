from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..serializers.change_password import UserChangePasswordSerializer

from ..renderers import UserRenderer


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )

        serializer.is_valid(raise_exception=True)
        return Response(
            {"data": "Password changed successfully"}, status=status.HTTP_200_OK
        )
