"""Forms for the multilingual_survey app."""
from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import six

from . import models


class SurveyForm(forms.Form):
    """
    Form that renders a survey and saves the returned answers.

    The form needs to be built fully dynamically since we don't know the number
    of questions and answers and we also don't know the type of the answers
    (multi-select vs. single-select).

    """
    def __init__(self, user, survey, data=None, files=None, auto_id='id_%s',
                 prefix=None, initial=None, error_class=forms.util.ErrorList,
                 label_suffix=':', empty_permitted=False):
        """
        Based on the given Survey, adds all necessary fields dynamically.

        Based on the given user, correctly sets initial values if the user
        has filled out this survey in the past.

        """
        self.user = user
        self.survey = survey
        self.base_fields = {}
        self.is_bound = data is not None or files is not None

        self.data = data or {}
        self.files = files or {}
        self.auto_id = auto_id
        self.prefix = prefix
        self.error_class = error_class
        self.label_suffix = label_suffix
        self.empty_permitted = empty_permitted
        self._errors = None
        self._changed_data = None
        # to maintain the order of questions, that by default order by position
        # field, we use the OrderedDict for adding fields.
        self.fields = OrderedDict()
        self.initial = initial or self.get_initial()

        for question in self.survey.questions.all():
            # First we add the select/multiselect for the question
            queryset = question.answers.all()
            field_kwargs = {
                'label': question.title,
                'queryset': queryset,
                'required': False,
            }

            if self.initial.get(question.slug):
                field_kwargs.update({'initial': self.initial.get(
                    question.slug)})
            if question.is_multi_select:
                self.fields[question.slug] = forms.ModelMultipleChoiceField(
                    **field_kwargs)
            else:
                self.fields[question.slug] = forms.ModelChoiceField(
                    **field_kwargs)

            # Then we add the `other` field for the question
            if question.has_other_field:
                self.fields[u'{0}_other'.format(question.slug)] = \
                    forms.CharField(
                        label=_('Other'),
                        max_length=2014,
                        required=False,
                    )

    def get_initial(self):
        initial = {}
        for question in self.survey.questions.all():
            try:
                response = self.user.responses.filter(
                    answer__question=question).distinct().get()
            except models.SurveyResponse.DoesNotExist:
                pass
            else:
                if not response.other_answer:
                    initial[question.slug] = [
                        resp.pk for resp in response.answer.all()]
                else:
                    initial[question.slug] = response.other_answer
        return initial

    def clean(self):
        for question in self.survey.questions.all():
            if question.required:
                response = self.cleaned_data.get(question.slug)
                if not response and (
                        not question.has_other_field or
                        not self.cleaned_data.get(
                        '{0}_other'.format(question.slug))):
                    self._errors[question.slug] = [_(
                        'This field is required.')]

        return self.cleaned_data

    def save(self):
        for question in self.survey.questions.all():
            # read the response from the cleaned data
            response = self.cleaned_data.get(question.slug)
            # if there is none but there is an other field, try again
            if not response and question.has_other_field:
                response = self.cleaned_data.get('{0}_other'.format(
                    question.slug))

            # if there was no response given in the data, remove the old one
            # and continue
            if not response:
                models.SurveyResponse.objects.filter(
                    user=self.user, question=question).delete()
                continue

            # otherwise check if there was a response. If not create one.
            try:
                user_response = models.SurveyResponse.objects.get(
                    user=self.user, question=question)
            except models.SurveyResponse.DoesNotExist:
                user_response = models.SurveyResponse.objects.create(
                    user=self.user, question=question)

            # Assign the answer to the user response object
            user_response.answer.clear()
            user_response.other_answer = ''
            if isinstance(response, six.string_types):
                user_response.other_answer = response
            else:
                for answer in response:
                    user_response.answer.add(answer)
            user_response.save()
        return self.survey
