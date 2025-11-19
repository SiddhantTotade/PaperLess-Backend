import os

from django.core.mail import EmailMessage

from types import SimpleNamespace


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            from_email=os.environ.get("EMAIL_FROM"),
            to=[data["to_email"]],
        )
        email.send()


def dict_to_namespace(data):
    if isinstance(data, dict):
        return SimpleNamespace(**{k: dict_to_namespace(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [dict_to_namespace(v) for v in data]
    else:
        return data
