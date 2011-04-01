from django.conf.urls.defaults import *

urlpatterns = patterns('course.views',
    # Example:
    # (r'^ListaOnline/', include('ListaOnline.foo.urls')),
	(r'^student/new$', 'new_student'),
	(r'^student/login$', 'student_login'),
)
