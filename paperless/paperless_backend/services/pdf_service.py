from django.template import Template as DjangoTemplate, Context
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .grpc_client import generate_pdf_via_grpc
import logging

logger = logging.getLogger(__name__)


class PDFService:

    @staticmethod
    def render_template(template_content, context_data):
        template = DjangoTemplate(template_content)
        context = Context(context_data)
        return template.render(context)
