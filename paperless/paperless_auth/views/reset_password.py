from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from ..serializers.reset_password import UserPasswordResetSerializer
from ..renderers import UserRenderer


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )

        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password reset successfully"}, status=status.HTTP_200_OK
        )
