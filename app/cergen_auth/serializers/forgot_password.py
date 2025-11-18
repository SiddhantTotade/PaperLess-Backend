from rest_framework import serializers
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from ..models import User
from ..utils import Util


class UserSendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f"http://localhost:3000/auth/reset-password/?uid={uid}&token={token}"
            body = f"""
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <div style="text-align: center;">
                    <img src="https://github.com/SiddhantTotade/CerGen-Frontend/blob/master/app_images/Paper.png" width="120" alt="Logo" />

                    <h2>Password Reset Request</h2>

                    <p>Click the button below to reset your password:</p>

                    <a href="{link}"
                        style="
                        display: inline-block;
                        padding: 12px 20px;
                        margin-top: 15px;
                        background-color: #4CAF50;
                        color: white;
                        text-decoration: none;
                        font-weight: bold;
                        border-radius: 6px;
                        ">
                        Reset Password
                    </a>

                    <p style="margin-top: 30px;">If you did not request this, ignore this email.</p>
                    </div>
                </body>
                </html>
                """

            data = {
                "email_subject": "Reset your password",
                "email_body": body,
                "to_email": user.email,
            }

            Util.send_mail(data)

            return attrs
        else:
            return serializers.ValidationError("You are not a registered user")
