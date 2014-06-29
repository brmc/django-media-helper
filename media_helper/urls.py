from django.conf.urls import patterns, include, url

from .views import resolution

urlpatterns = patterns('',
    url(r'^resolution/', resolution, name = "resolution"),
)
