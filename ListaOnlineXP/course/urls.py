# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'course.views',
    (r'^course/([0-9]+)/$', 'course'),
    (r'^course/$', 'course_list'),
)
