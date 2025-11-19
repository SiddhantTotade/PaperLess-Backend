from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(SendersCredentials)
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(EventFile)
admin.site.register(CompletionCertificateTemplate)
admin.site.register(MeritCertificateTemplate)
admin.site.register(ContributedCompletionCertificates)
admin.site.register(ContributedMeritCertificates)
admin.site.register(ParticipantAlbum)
admin.site.register(Template)
