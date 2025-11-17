from ..models import User
from rest_framework import serializers


# User change password serializer
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input-type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input-type": "password2"}, write_only=True
    )

    class Meta:
        models = User
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        user = self.context.get("user")

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password is not matching"
            )

        user.set_password(password)
        user.save()

        return attrs
