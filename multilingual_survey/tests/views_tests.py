"""Tests for the views of the ``multilingual_survey`` app."""
from django.conf import settings
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewRequestFactoryTestMixin

from . import factories
from .. import views


class SurveyReportAdminViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``SurveyReportAdminView`` view class."""
    view_class = views.SurveyReportAdminView

    def get_view_kwargs(self):
        return {'slug': self.survey.slug}

    def setUp(self):
        self.admin = UserFactory(is_staff=True)
        self.user = UserFactory()
        self.survey = factories.SurveyFactory()

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        # should also redirect to login for regular users
        self.redirects(user=self.user, to='{0}?next={1}'.format(
                       settings.LOGIN_URL, self.get_url()))
        self.is_callable(user=self.admin)
