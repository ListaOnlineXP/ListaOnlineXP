# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from views import GetStudentsExerciseList

urlpatterns = patterns(
    'exerciselist.views',
    (r'^get_code/$', 'get_code'),
    (r'^my_exercise_lists/$', GetStudentsExerciseList.as_view()),
    (r'^view_exercise_list/(?P<exercise_list_id>\d+)/$', 'exercise_list'),
)
