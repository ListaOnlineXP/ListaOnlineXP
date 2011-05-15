# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'', include('authentication.urls')),
    (r'', include('course.urls')),
    (r'', include('exerciselist.urls')),
)

#Serve the static files in the development environment
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_DOC_ROOT}),
    )
