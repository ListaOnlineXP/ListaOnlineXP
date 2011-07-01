# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'course.views',
    (r'^course/$', 'course_list'),
    (r'^course/add/$', 'course_add_or_update'),
    (r'^course/update/([0-9]+)/$', 'course_add_or_update'),
    (r'^course/delete/([0-9]+)/$', 'course_delete'),
    (r'^course/([0-9]+)/$', 'course'),
    (r'^course/([0-9]+)/report/$', 'report'),
    (r'^my/course/$', 'my_course_list'),
)
