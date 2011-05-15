# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('course.views',
    (r'^$', 'course_list'),
    (r'^course/([0-9]+)/$', 'course'),
    (r'^course/enroll/([0-9]+)/$', 'course_enroll'),
    (r'^course/$', 'course_list'),
)
