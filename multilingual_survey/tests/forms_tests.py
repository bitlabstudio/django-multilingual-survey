"""Tests for the forms of the multilingual_survey app."""
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from mixer.backend.django import mixer

from .. import forms
from .. import models


class SurveyFormTestCase(TestCase):
    """Tests for the ``SurveyForm``."""
    longMessage = True

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.answer1 = mixer.blend(
            'multilingual_survey.SurveyAnswerTranslation',
            language_code='en').master
        self.question1 = self.answer1.question
        self.survey = self.question1.survey
        self.question2 = mixer.blend(
            'multilingual_survey.SurveyQuestionTranslation',
            survey=self.survey, has_other_field=True,
            language_code='en').master
        mixer.blend(
            'multilingual_survey.SurveyResponse',
            other_answer='Foo', question=self.question2, language_code='en',
            user=self.user)
        self.question3 = mixer.blend(
            'multilingual_survey.SurveyQuestionTranslation',
            survey=self.survey, is_multi_select=True, has_other_field=True,
            required=True, language_code='en').master
        self.answer3_1 = mixer.blend(
            'multilingual_survey.SurveyAnswerTranslation',
            language_code='en',
            question=self.question3).master
        self.answer3_2 = mixer.blend(
            'multilingual_survey.SurveyAnswerTranslation',
            language_code='en',
            question=self.question3).master
        self.question4 = mixer.blend(
            'multilingual_survey.SurveyQuestionTranslation',
            language_code='en',
            survey=self.survey).master
        self.answer4 = mixer.blend(
            'multilingual_survey.SurveyAnswerTranslation',
            language_code='en',
            question=self.question4).master

        self.data = {
            # question 1 was not required
            self.question1.slug: [],
            '{0}_other'.format(self.question2.slug): 'Foo',
            self.question3.slug: [self.answer3_1.pk],
            self.question4.slug: self.answer4.pk,
        }

    def test_form_with_user(self):
        form = forms.SurveyForm(self.user, 'foo', self.survey)
        self.assertTrue(self.question1.slug in form.fields.keys(), msg=(
            'Should dynamically add fields for all questions to the form'))
        self.assertFalse(
            self.question1.slug + '_other' in form.fields.keys(), msg=(
                'Should not add `other` field if the question has not enabled'
                ' it'))

        """
        TODO: Fix the following tests:

        self.assertTrue(self.question3.slug in form.fields.keys(), msg=(
            'Should dynamically add fields for all questions to the form'))
        self.assertTrue(
            self.question3.slug + '_other' in form.fields.keys(), msg=(
                'Should dynamically add `other` field if the question has'
                ' enabled it'))

        """

        form = forms.SurveyForm(self.user, 'foo', self.survey, self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        valid_data = {
            # question 1 was not required
            self.question1.slug: [],
            '{0}_other'.format(self.question2.slug): 'Foo',
            '{0}_other'.format(self.question3.slug): 'Something',
        }
        form = forms.SurveyForm(self.user, 'foo', self.survey, valid_data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        # one question is required and the other is not, so not passing
        # anything should make it invalid
        bad_data = {}
        form = forms.SurveyForm(self.user, 'foo', self.survey, bad_data)
        """
        TODO: Fix the following tests:

        self.assertFalse(form.is_valid(), msg='The form should not be valid.')

        """

        self.question3.has_other_field = False
        self.question3.save()
        form = forms.SurveyForm(self.user, 'foo', self.survey, self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        form.save()
        """
        TODO: Fix the following tests:

        self.assertEqual(models.SurveyResponse.objects.count(), 3, msg=(
            'When saved, there should be three responses in the database.'))

        """

        valid_data = self.data.copy()
        valid_data.update({self.question1.slug: self.answer1.pk})
        form = forms.SurveyForm(self.user, 'foo', self.survey, valid_data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should still be valid. Errors: {0}'.format(form.errors)))
        form.save()
        """
        TODO: Fix the following tests:

        self.assertEqual(models.SurveyResponse.objects.count(), 4, msg=(
            'When saved again with more responses, there should be 4'
            ' responses in the database.'))

        self.assertEqual(
            form.initial[self.question3.slug], [self.answer3_1.pk], msg=(
                'If no data given, the form should add the already known'
                ' answers from the database'))

        """

    def test_form_with_anonymous(self):
        form = forms.SurveyForm(AnonymousUser(), 'foo', self.survey, self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))
        form.save()
        self.assertEqual(models.SurveyResponse.objects.count(), 1, msg=(
            'When saved, there should be 1 response in the database.'))
