from rest_framework.response import Response
from rest_frameworks.views import APIView

from models import *


class GenerateEventTemplateAPIView(APIView):
    def post(self, request):
        try:
            event_id = request.data.get("event_id")
            template_id = request.data.get("template_id")
            orientation = request.data.get("orientation", "portrait")

            if not event_id or not template_id:
                return Response(
                    {
                        "success": False,
                        "message": "event_id and template_id are required.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            event = Event.objects.get(id=event_id)
            template_obj = Template.objects.get(id=template_id, user=event.user)

            event_details = {}
            if hasattr(event, "details") and event.details:
                try:
                    if isinstance(event.details, str):
                        event_details = json.loads(event.details)
                    elif isinstance(event.details, dict):
                        event_details = event.details
                except Exception as e:
                    print("Invalid JSON in event.details:", e)

            event_obj = dict_to_namespace(event_details)

            html_template = DjangoTemplate(template_obj.html_content or "")
            context = Context({"e": event_obj})
            rendered_html = html_template.render(context)

            html_clean = rendered_html.replace("\r", "").replace("\n", "")
            pdf_bytes = generate_pdf_via_grpc(template_id, html_clean, orientation)
            encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

            return Response(
                {
                    "success": True,
                    "message": "Event template generated successfully.",
                    "data": {
                        "html": rendered_html,
                        "pdf_data": encoded_pdf,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Event.DoesNotExist:
            return Response(
                {"success": False, "message": "Event not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Template.DoesNotExist:
            return Response(
                {"success": False, "message": "Template not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
