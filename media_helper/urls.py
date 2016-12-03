from django.conf.urls import url

from .views import media_helper

urlpatterns = (
    url(r'^resize/', media_helper, name="media_helper"),
)
