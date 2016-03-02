"""Tests for the templatetags of the ``multilingual_survey`` app."""
from django.test import TestCase

from mixer.backend.django import mixer

from ..templatetags import survey_tags


class FilterResponsesTestCase(TestCase):
    """Tests for the ``filter_responses`` tamplatetag."""
    longMessage = True

    def test_tag(self):
        answer = mixer.blend(
            'multilingual_survey.SurveyAnswerTranslation').master
        response_1 = mixer.blend('multilingual_survey.SurveyResponse',
                                 question=answer.question)
        response_1.answer.add(answer)
        response_2 = mixer.blend('multilingual_survey.SurveyResponse',
                                 question=answer.question)
        response_2.answer.add(answer)
        self.assertEqual(
            survey_tags.filter_responses(answer, [], []).count(), 2,
            msg=('Should return two responses.'))
        self.assertEqual(
            survey_tags.filter_responses(
                answer, [], [response_2.session_id]).count(),
            1, msg=('Should return one response.'))
