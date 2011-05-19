# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'course.views',
    (r'^course/$', 'course_list'),
    (r'^course/add/$', 'course_add_or_update'),
    (r'^course/([0-9]+)/$', 'course'),
)
