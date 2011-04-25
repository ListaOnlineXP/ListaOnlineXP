# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'exerciselist.views',
    (r'^get_code/$', 'get_code'),
    (r'^course/([0-9]+)/([0-9]+)$', 'exercise_list'),
)
