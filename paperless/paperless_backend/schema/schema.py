import graphene

from ..schema import (
    event_schema,
    participant_schema,
    template_schema,
)

EventQuery = event_schema.Query
ParticipantQuery = participant_schema.Query
TemplateQuery = template_schema.Query


class Query(EventQuery, ParticipantQuery, TemplateQuery, graphene.ObjectType):
    pass


EventMutation = event_schema.Mutation
ParticipantMutation = participant_schema.Mutation
TemplateMutation = template_schema.Mutation


class Mutation(
    EventMutation, ParticipantMutation, TemplateMutation, graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
