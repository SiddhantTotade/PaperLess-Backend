from rest_framework.serializers import ModelSerializer, SerializerMethodField
from ..models import User


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email",]