import os
import string
import random
from django.db import models
from django.utils.translation import gettext as _
from paperless_auth.models import User


# Create your models here.


def generate_random_string():
    str = "".join(random.choices(string.ascii_lowercase, k=10))
    return str


def convert_to_img(file_name):

    ppt_to_image_command = f"unoconv -f jpg certificate-data/{file_name}"
    os.system(ppt_to_image_command)

    img_file_name = os.path.splitext(str(file_name))[0]

    return f"{img_file_name}.jpg"


class SendersCredentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    senders_email = models.EmailField(null=True, blank=True)
    senders_password = models.CharField(max_length=255, null=True, blank=True)
    senders_phone = models.CharField(max_length=13, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.CharField(max_length=20, null=True, blank=True)
    details = models.JSONField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event or 'Event'} (ID: {self.id})"


class EventFile(models.Model):
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE)
    xlsx_file = models.FileField(
        upload_to="certificates/csv_files/", null=True, blank=True
    )


class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant_details = models.JSONField(default=None)

    def __str__(self):
        return str(self.id)


class Template(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template_name = models.CharField(max_length=20, null=True, blank=True)
    html_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.template_name


class CompletionCertificateTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    template = models.FileField(upload_to="completion-certificate-templates/")
    template_img = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.template_img = convert_to_img(self.template.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class MeritCertificateTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    template = models.FileField(upload_to="merit-certificate-templates/")
    template_img = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.template_img = convert_to_img(self.template)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class ContributedCompletionCertificates(models.Model):
    template = models.FileField(
        upload_to="contributed-completion-certificate-templates/"
    )
    template_img = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.template_img = convert_to_img(self.template)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class ContributedMeritCertificates(models.Model):
    template = models.FileField(upload_to="contributed-merit-certificate-templates/")
    template_img = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.template_img = convert_to_img(self.template)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class ParticipantAlbum(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    image_album = models.ImageField(upload_to="image-album/", null=True, blank=True)
