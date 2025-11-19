from rest_framework.authentication import *
from paperless_auth.authentication import CustomJWTAuthentication
from graphene_django.views import GraphQLView


class AuthenticatedGraphQlView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        user = None
        auth_classes = [CustomJWTAuthentication]

        for auth_class in auth_classes:
            auth = auth_class()
            try:
                user_auth_tuple = auth.authenticate(request)
                if user_auth_tuple:
                    user, _ = user_auth_tuple
                    break
            except Exception as e:
                print("Auth error:", e)
        request.user = user or request.user
        return super().dispatch(request, *args, **kwargs)
