# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('authentication.views',
    (r'^$', 'home'),
    (r'^login/$', login, {'template_name' : 'login.html'}),
    (r'^logout/$', logout, {'next_page': '/login/'}),
    (r'^signup/$', 'signup'),
)
