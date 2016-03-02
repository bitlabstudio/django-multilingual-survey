"""URLs to run the tests."""
from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^pos/', include('generic_positions.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('multilingual_survey.urls')),
]
