"""URLs for the multilingual_survey app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^report/(?P<slug>[\w-]+)/$',
        views.SurveyReportAdminView.as_view(),
        name='multilingual_survey_admin_report'),
)
