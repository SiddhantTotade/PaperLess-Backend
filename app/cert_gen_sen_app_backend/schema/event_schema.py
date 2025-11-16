import graphene
from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar
from graphql import GraphQLError

from ..models import Event, Participant


class EventKeysType(graphene.ObjectType):
    detail_keys = graphene.List(graphene.String)
    participant_detail_keys = graphene.List(graphene.String)


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = (
            "id",
            "user",
            "event",
            "details",
            "created_at",
            "updated_at",
        )


class Query(graphene.ObjectType):
    events = graphene.List(EventType)
    event = graphene.Field(EventType, id=graphene.Int(required=True))
    event_data = graphene.Field(EventKeysType, event_id=graphene.Int(required=True))

    def resolve_events(self, info):
        user = info.context.user
        if not user or not user.is_authenticated:
            return Event.objects.none()
        return Event.objects.filter(user=user).order_by("-id")

    def resolve_event(self, info, id):
        user = info.context.user
        if not user or not user.is_authenticated:
            return None
        try:
            return Event.objects.get(id=id, user=user)
        except Event.DoesNotExist:
            return None

    def resolve_event_data(self, info, event_id):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise GraphQLError("Authentication required.")

        try:
            event = Event.objects.get(id=event_id, user=user)
        except Event.DoesNotExist:
            raise GraphQLError("Event not found or not accessible.")

        detail_keys = (
            list(event.details.keys()) if isinstance(event.details, dict) else []
        )

        participants = Participant.objects.filter(event=event)
        participant_keys = set()

        for p in participants:
            if isinstance(p.participant_details, dict):
                participant_keys.update(p.participant_details.keys())

        return EventKeysType(
            detail_keys=detail_keys,
            participant_detail_keys=list(participant_keys),
        )


class CreateEvent(graphene.Mutation):
    event = graphene.Field(EventType)

    class Arguments:
        event = graphene.String(required=True)
        details = GenericScalar(required=True)

    def mutate(self, info, event, details=None):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise Exception("Authentication required")

        event_obj = Event.objects.create(
            user=user,
            event=event,
            details=details or {},
        )
        return CreateEvent(event=event_obj)


class UpdateEvent(graphene.Mutation):
    event = graphene.Field(EventType)

    class Arguments:
        id = graphene.Int(required=True)
        event = graphene.String(required=True)
        details = GenericScalar(required=True)

    def mutate(self, info, id, event=None, details=None):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise Exception("Authentication required")

        try:
            event_obj = Event.objects.get(id=id, user=user)
        except Event.DoesNotExist:
            raise Exception("Event not found")

        if event is not None:
            event_obj.event = event
        if details is not None:
            event_obj.details = details

        event_obj.save()
        return UpdateEvent(event=event_obj)


class DeleteEvent(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        ids = graphene.List(graphene.Int, required=True)

    def mutate(self, info, ids):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise Exception("Authentication required")

        events = Event.objects.filter(id__in=ids, user=user)

        if not events.exists():
            raise Exception("No events found for the given IDs")

        events.delete()

        return DeleteEvent(ok=True)


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()
