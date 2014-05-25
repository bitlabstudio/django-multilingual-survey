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
