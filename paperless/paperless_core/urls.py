from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    # REST APIs -- For authentication and template generation
    path("auth/api/", include("paperless_auth.urls")),
    path("app/api/", include("paperless_backend.urls")),
    # GraphQL APIs -- For application
    path("graphql/", include("paperless_backend.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
