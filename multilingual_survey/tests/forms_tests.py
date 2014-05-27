"""Tests for the forms of the multilingual_survey app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from .. import forms
from . import factories


class SurveyFormTestCase(TestCase):
    """Tests for the ``SurveyForm``."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.answer1 = factories.SurveyAnswerFactory()
        self.question1 = self.answer1.question
        self.survey = self.question1.survey
        self.answer2 = factories.SurveyAnswerFactory()
        self.question2 = factories.SurveyQuestionFactory(
            survey=self.survey, is_multi_select=True, has_other_field=True)
        self.answer2_1 = factories.SurveyAnswerFactory(question=self.question2)
        self.answer2_2 = factories.SurveyAnswerFactory(question=self.question2)
        self.response1 = factories.SurveyResponseFactory(
            user=self.user, answer=self.answer1)
        self.response2 = factories.SurveyResponseFactory(
            user=self.user, question=self.question2, other_answer='Foobar')

    def test_form(self):
        form = forms.SurveyForm(self.user, self.survey)
        self.assertTrue(self.question1.slug in form.fields.keys(), msg=(
            'Should dynamically add fields for all questions to the form'))
        self.assertFalse(
            self.question1.slug + '_other' in form.fields.keys(), msg=(
                'Should not add `other` field if the question has not enabled'
                ' it'))

        self.assertTrue(self.question2.slug in form.fields.keys(), msg=(
            'Should dynamically add fields for all questions to the form'))
        self.assertTrue(
            self.question2.slug + '_other' in form.fields.keys(), msg=(
                'Should dynamically add `other` field if the question has'
                ' enabled it'))

        self.assertEqual(
            form.data[self.question1.slug], [self.answer1.pk], msg=(
                'If no data given, the form should add the already known'
                ' answers from the database'))

        # self.assertEqual(
        #     form.data[self.question2.slug + '_other'], 'Foobar', msg=(
        #         'If no data given, the form should add the already known'
        #         ' other-answers from the database'))
