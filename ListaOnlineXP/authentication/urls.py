# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib.auth.views import logout


urlpatterns = patterns('authentication.views',
    (r'^login/$', 'login'),
    (r'^logout/$', logout, {'next_page': '/login/'}),
    (r'^signup/$', 'signup'),
)
