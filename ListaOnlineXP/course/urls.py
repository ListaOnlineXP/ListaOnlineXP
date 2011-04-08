# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'course.views',
    # Example:
    # (r'^ListaOnline/', include('ListaOnline.foo.urls')),
	(r'^student/$', 'student'),
    (r'^student/new/$', 'new_student'),
    (r'^student/login/$', 'student_login'),
	(r'^student/logout/$', 'student_logout'),
    (r'^courses/$', 'course_list'),
    (r'^get_code/$', 'get_code'),    
)
