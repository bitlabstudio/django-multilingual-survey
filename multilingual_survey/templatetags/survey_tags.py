"""Templatetags for the ``multilingual_survey`` app."""
from django import template


register = template.Library()


@register.assignment_tag()
def filter_responses(answer, user_selection, session_selection):
    """Returns the respons count for a specific user selection."""
    if user_selection or session_selection:
        responses = answer.responses.filter(
            user__pk__in=user_selection) | answer.responses.filter(
                session_id__in=session_selection)
        return responses.distinct()
    return answer.responses.all()
