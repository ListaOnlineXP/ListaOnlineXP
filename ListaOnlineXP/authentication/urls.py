# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'authentication.views',
    (r'^$', 'home'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    (r'^signup/$', 'signup'),
)

