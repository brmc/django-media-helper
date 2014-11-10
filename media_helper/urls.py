from django.conf.urls import patterns, url

from .views import media_helper

urlpatterns = patterns(
    '',
    url(r'^resize/', media_helper, name="media_helper"),
)
