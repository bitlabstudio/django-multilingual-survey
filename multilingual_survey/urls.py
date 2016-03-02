"""URLs for the multilingual_survey app."""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^report/(?P<slug>[\w-]+)/$',
        views.SurveyReportAdminView.as_view(),
        name='multilingual_survey_admin_report'),
    url(r'^report/$',
        views.SurveyReportListView.as_view(),
        name='multilingual_survey_list_report'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.SurveyView.as_view(),
        name='multilingual_survey_detail'),
]
