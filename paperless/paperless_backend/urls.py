from django.views.decorators.csrf import csrf_exempt
from .views import generate_event, generate_participant, authenticate_graphql
from django.urls import path
from .schema.schema import schema

AuthenticatedGraphQlView = authenticate_graphql.AuthenticatedGraphQlView
GenerateEventTemplateAPIView = generate_event.GenerateEventTemplateAPIView
GenerateParticipantTemplateAPIView = (
    generate_participant.GenerateParticipantTemplateAPIView
)

urlpatterns = [
    path("api/", AuthenticatedGraphQlView.as_view(graphiql=True, schema=schema)),
    path("generate-event/", GenerateEventTemplateAPIView.as_view()),
    path("generate-participants/", GenerateParticipantTemplateAPIView.as_view()),
]
