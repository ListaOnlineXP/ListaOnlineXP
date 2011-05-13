# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

# Enable admin site
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    #Enable admin site
    (r'^admin/', include(admin.site.urls)),
    #(r'', include('course.urls')),
    #(r'', include('exerciselist.urls')),
    (r'', include('authentication.urls')),
)


#Serve the static files in the development environment
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_DOC_ROOT}),
    )
