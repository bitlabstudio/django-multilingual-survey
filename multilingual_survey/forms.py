"""Forms for the multilingual_survey app."""
from django import forms


class SurveyForm(forms.Form):
    """
    Form that renders a survey and saves the returned answers.

    The form needs to be built fully dynamically since we don't know the number
    of questions and answers and we also don't know the type of the answers
    (multi-select vs. single-select).

    """
    def __init__(self, user, survey, *args, **kwargs):
        self.user = user
        self.survey = survey
        super(SurveyForm, self).__init__(*args, **kwargs)
        for question in self.survey.questions.all():
            # First we add the select/multiselect for the question
            queryset = question.answers.all()
            field_kwargs = {
                'queryset': queryset,
                'required': False,
            }
            if question.is_multi_select:
                self.fields[question.slug] = forms.ModelMultipleChoiceField(
                    **field_kwargs)
            else:
                self.fields[question.slug] = forms.ModelChoiceField(
                    **field_kwargs)

            # Then we add the `other` field for the question
            self.fields['{0}_other'.format(question.slug)] = forms.CharField(
                max_length=2014, required=False)
