"""Forms for the multilingual_survey app."""
from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _

from generic_positions.templatetags.position_tags import order_by_position

from . import models

try:
    # Django < 1.7.x
    from django.forms.util import ErrorList
except ImportError:
    # Django >= 1.7.x
    from django.forms.utils import ErrorList


class SurveyForm(forms.Form):
    """
    Form that renders a survey and saves the returned answers.

    The form needs to be built fully dynamically since we don't know the number
    of questions and answers and we also don't know the type of the answers
    (multi-select vs. single-select).

    """
    def __init__(self, user, session_key, survey, data=None, files=None,
                 auto_id='id_%s', prefix=None, initial=None, label_suffix=':',
                 error_class=ErrorList, empty_permitted=False):
        """
        Based on the given Survey, adds all necessary fields dynamically.

        Based on the given user, correctly sets initial values if the user
        has filled out this survey in the past.

        """
        self.user = user if user.is_authenticated() else None
        self.session_key = session_key
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
        # To maintain the order of questions, that by default order by position
        # field, we use the OrderedDict for adding fields.
        self.fields = OrderedDict()
        self._bound_fields_cache = {}
        self.initial = initial or self.get_initial()

        for question in order_by_position(self.survey.questions.all()):
            # First we add the select/multiselect for the question
            queryset = question.answers.all()
            if queryset:
                field_kwargs = {
                    'label': question.__unicode__(),
                    'queryset': queryset.order_by(
                        'generic_position__position'),
                    'required': False,
                }

                if self.initial.get(question.slug):
                    field_kwargs.update({'initial': self.initial.get(
                        question.slug)})

                if question.is_multi_select:
                    field_kwargs.update({
                        'widget': forms.CheckboxSelectMultiple,
                    })
                    self.fields.update({
                        question.slug: forms.ModelMultipleChoiceField(
                            **field_kwargs)})
                else:
                    self.fields.update({
                        question.slug: forms.ModelChoiceField(**field_kwargs)})

                # Then we add the `other` field for the question
                if question.has_other_field:
                    field_name = u'{0}_other'.format(question.slug)
                    self.fields.update({
                        field_name: forms.CharField(
                            label=_('Other'), max_length=2014,
                            required=False)})
                    self.fields[field_name].widget.attrs.update({
                        'data-class': 'other-field'})
            elif question.has_other_field:
                self.fields.update({
                    u'{0}_other'.format(question.slug): forms.CharField(
                        label=question.__unicode__(), max_length=2014,
                        required=question.required,
                        initial=self.initial.get(question.slug))})

    def get_initial(self):
        initial = {}
        for question in self.survey.questions.all():
            if self.user:
                try:
                    response = self.user.responses.filter(
                        question=question).distinct().get()
                except models.SurveyResponse.DoesNotExist:
                    continue
            else:
                try:
                    response = models.SurveyResponse.objects.filter(
                        question=question,
                        session_id=self.session_key,
                        user__isnull=True,
                    ).distinct().get()
                except models.SurveyResponse.DoesNotExist:
                    continue
            if not response.other_answer:
                if question.is_multi_select:
                    initial[question.slug] = [
                        resp.pk for resp in response.answer.all()]
                elif response.answer.all():
                    initial[question.slug] = response.answer.all()[0].pk
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
            other_response = False
            if question.has_other_field:
                other_response = self.cleaned_data.get('{0}_other'.format(
                    question.slug))

            # if there was no response given in the data, remove the old one
            # and continue
            if not response and not other_response:
                if self.user:
                    models.SurveyResponse.objects.filter(
                        user=self.user,
                        question=question,
                    ).delete()
                else:
                    models.SurveyResponse.objects.filter(
                        user__isnull=True,
                        session_id=self.session_key,
                        question=question,
                    ).delete()
                continue

            # otherwise check if there was a response. If not create one.
            if self.user:
                resp_obj, crtd = models.SurveyResponse.objects.get_or_create(
                    user=self.user, question=question)
            else:
                resp_obj, crtd = models.SurveyResponse.objects.get_or_create(
                    user__isnull=True, session_id=self.session_key,
                    question=question)

            # Assign the answer to the user response object
            resp_obj.answer.clear()
            resp_obj.other_answer = ''
            if other_response:
                resp_obj.other_answer = other_response
            if response:
                if isinstance(response, models.SurveyAnswer):
                    resp_obj.answer.add(response)
                else:
                    for answer in response:
                        resp_obj.answer.add(answer)
            resp_obj.save()
        return self.survey
