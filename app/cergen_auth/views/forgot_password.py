from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..renderers import UserRenderer
from ..serializers.forgot_password import UserSendPasswordResetEmailSerializer


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserSendPasswordResetEmailSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password reset link has been sent on your e-mail"},
            status=status.HTTP_200_OK,
        )
