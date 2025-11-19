import json
import base64

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.template import Template as DjangoTemplate, Context

from types import SimpleNamespace

from ..services.grpc_client import generate_pdf_via_grpc


from ..models import Event, Template, Participant


def dict_to_namespace(data):
    if isinstance(data, dict):
        return SimpleNamespace(**{k: dict_to_namespace(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [dict_to_namespace(v) for v in data]
    else:
        return data


class GenerateParticipantTemplateAPIView(APIView):
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
            if event.details:
                try:
                    if isinstance(event.details, str):
                        event_details = json.loads(event.details)
                    elif isinstance(event.details, dict):
                        event_details = event.details
                except Exception as e:
                    print("Invalid JSON in event.details:", e)

            event_obj = dict_to_namespace(event_details)

            participants = Participant.objects.filter(event=event)
            if not participants.exists():
                return Response(
                    {
                        "success": False,
                        "message": "No participants found for this event.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            rendered_outputs = []

            for participant in participants:
                participant_details = {}
                if participant.participant_details:
                    try:
                        if isinstance(participant.participant_details, str):
                            participant_details = json.loads(
                                participant.participant_details
                            )
                        elif isinstance(participant.participant_details, dict):
                            participant_details = participant.participant_details
                    except Exception as e:
                        print("Invalid JSON in participant_details:", e)

                participant_obj = dict_to_namespace(participant_details)

                html_template = DjangoTemplate(template_obj.html_content or "")
                context = Context({"e": event_obj, "p": participant_obj})
                rendered_html = html_template.render(context)
                html_clean = rendered_html.replace("\r", "").replace("\n", "")

                pdf_bytes = generate_pdf_via_grpc(template_id, html_clean, orientation)
                encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

                rendered_outputs.append(
                    {
                        "participant_id": participant.id,
                        "html": rendered_html,
                        "pdf_data": encoded_pdf,
                    }
                )

            return Response(
                {
                    "success": True,
                    "message": "Templates generated for all participants.",
                    "data": rendered_outputs,
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
            print("Unexpected error:", e)
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
