import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from ..models import Template


class TemplateType(DjangoObjectType):
    class Meta:
        model = Template
        fields = (
            "id",
            "template_name",
            "html_content",
            "created_at",
            "updated_at",
        )


class Query(graphene.ObjectType):
    templates = graphene.List(TemplateType)
    template = graphene.Field(TemplateType, id=graphene.Int(required=True))

    def resolve_templates(self, info):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required.")
        return Template.objects.filter(user=user).order_by("-id")

    def resolve_template(self, info, id):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required.")
        try:
            return Template.objects.get(id=id, user=user)
        except Template.DoesNotExist:
            raise GraphQLError("Template not found or not accessible.")


class CreateTemplate(graphene.Mutation):
    class Arguments:
        template_name = graphene.String(required=True)
        html_content = graphene.String(required=True)

    template = graphene.Field(TemplateType)

    def mutate(self, info, template_name, html_content):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required.")

        template = Template.objects.create(
            user=user, template_name=template_name, html_content=html_content
        )
        return CreateTemplate(template=template)


class UpdateTemplate(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        template_name = graphene.String(required=False)
        html_content = graphene.String(required=False)

    template = graphene.Field(TemplateType)

    def mutate(self, info, id, template_name=None, html_content=None):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required.")

        try:
            template = Template.objects.get(id=id, user=user)
        except Template.DoesNotExist:
            raise GraphQLError("Template not found or not accessible.")

        if template_name:
            template.template_name = template_name
        if html_content:
            template.html_content = html_content

        template.save()
        return UpdateTemplate(template=template)


class DeleteTemplate(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        ids = graphene.List(graphene.Int, required=True)

    def mutate(self, info, ids):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise GraphQLError("Authentication required.")

        template = Template.objects.filter(id__in=ids, user=user)

        template.delete()

        return DeleteTemplate(ok=True)


class Mutation(graphene.ObjectType):
    create_template = CreateTemplate.Field()
    update_template = UpdateTemplate.Field()
    delete_template = DeleteTemplate.Field()
