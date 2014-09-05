from django.conf.urls import patterns, include

import media_helpdder
#api.autodiscover()

urlpatterns = patterns('',
    (r'^media-helper/resolution/', include(media_helper.urls)),
)
