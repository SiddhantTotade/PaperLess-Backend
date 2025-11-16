import graphene
from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar

from ..models import Participant, Event


class ParticipantType(DjangoObjectType):
    class Meta:
        model = Participant
        fields = ("id", "event", "participant_details")


class Query(graphene.ObjectType):
    all_participants = graphene.List(
        ParticipantType,
        event_id=graphene.Int(required=False),
    )
    participant = graphene.Field(ParticipantType, id=graphene.Int(required=True))

    def resolve_all_participants(self, info, event_id=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        qs = Participant.objects.all()
        if event_id:
            qs = qs.filter(event__id=event_id)
        return qs


class CreateParticipant(graphene.Mutation):
    class Arguments:
        event_id = graphene.Int(required=True)
        participant_details = GenericScalar(required=True)

    participant = graphene.Field(ParticipantType)

    def mutate(self, info, event_id, participant_details):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        event = Event.objects.get(pk=event_id)
        participant = Participant.objects.create(
            event=event, participant_details=participant_details
        )
        return CreateParticipant(participant=participant)


class UpdateParticipant(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        participant_details = graphene.JSONString(required=True)

    participant = graphene.Field(ParticipantType)

    def mutate(self, info, id, participant_details):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        participant = Participant.objects.get(pk=id)
        participant.participant_details = participant_details
        participant.save()
        return UpdateParticipant(participant=participant)


class DeleteParticipant(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        ids = graphene.List(graphene.Int, required=True)

    def mutate(self, info, ids):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        participant = Participant.objects.filter(id__in=ids)

        participant.delete()

        return DeleteParticipant(ok=True)


class Mutation(graphene.ObjectType):
    create_participant = CreateParticipant.Field()
    update_participant = UpdateParticipant.Field()
    delete_participant = DeleteParticipant.Field()
