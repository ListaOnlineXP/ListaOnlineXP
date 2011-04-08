# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'course.views',
	(r'^$', 'home'),
    (r'^login/$', 'login'),
	(r'^logout/$', 'logout'),
    (r'^signup/$', 'signup'),
    (r'^courses/$', 'course_list'),
    (r'^get_code/$', 'get_code'),    
)
