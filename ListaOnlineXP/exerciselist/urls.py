# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from views import GetStudentsExerciseList
urlpatterns = patterns(
    'exerciselist.views',
    (r'^get_code/$', 'get_code'),
    (r'^course/([0-9]+)/([0-9]+)$', 'exercise_list'),
    (r'^my_exercise_lists/$', GetStudentsExerciseList.as_view()),
    (r'^exercise_list/(?P<exercise_list_id>\d+)/$', 'view_java_questions'),
)
