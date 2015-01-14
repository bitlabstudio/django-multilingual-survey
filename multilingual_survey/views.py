"""Views for the multilingual_survey app."""
from django.views.generic import DetailView, FormView, ListView
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.utils.decorators import method_decorator

from . import forms
from . import models


class SurveyReportAdminView(DetailView):
    """A view to display results of a survey for admins."""
    model = models.Survey
    template_name = 'multilingual_survey/survey_report_admin.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(SurveyReportAdminView, self).dispatch(
            request, *args, **kwargs)


class SurveyReportListView(ListView):
    """A view to display a list of surveys for admins."""
    model = models.Survey
    template_name = 'multilingual_survey/survey_report_list.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(SurveyReportListView, self).dispatch(
            request, *args, **kwargs)


class SurveyView(FormView):
    """A view to display a survey."""
    form_class = forms.SurveyForm
    template_name = 'multilingual_survey/survey_detail.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.survey = models.Survey.objects.get(slug=kwargs['slug'])
        except models.Survey.DoesNotExist:
            raise Http404
        return super(SurveyView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SurveyView, self).get_context_data(**kwargs)
        context.update({'survey': self.survey})
        return context

    def get_form_kwargs(self):
        kwargs = super(SurveyView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            'survey': self.survey,
        })
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context.update({'success': True})
        return self.render_to_response(context)
