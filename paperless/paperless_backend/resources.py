from import_export import resources
from .models import *

class ParticipantResource(resources.ModelResource):
    class Meta:
        model = Participant