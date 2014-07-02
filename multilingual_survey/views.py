"""Views for the multilingual_survey app."""
from django.views.generic import DetailView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from . import models


class SurveyReportAdminView(DetailView):
    """A view to display results of a survey for admins."""
    model = models.Survey
    template_name = 'multilingual_survey/survey_report_admin.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(SurveyReportAdminView, self).dispatch(
            request, *args, **kwargs)
