import json
from django.template import Template as DjangoTemplate, Context


def modify(event_id, image):
    dict = {}
    dict["event"] = image
    return dict


class TemplateRenderHelper:

    @staticmethod
    def render_html(template_html, event, participant=None):
        def safe_json(data):
            if isinstance(data, str):
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    return {}
            return data or {}

        event_details = safe_json(event.details)
        participant_details = safe_json(getattr(participant, "participant_details", {}))

        context_data = {
            "event": {"id": event.id, "name": event.event, **event_details},
        }

        if participant:
            context_data["participant"] = {"id": participant.id, **participant_details}

        template = DjangoTemplate(template_html)
        rendered_html = template.render(Context(context_data))
        return rendered_html
