# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from views import GetStudentsExerciseList

urlpatterns = patterns(
    'exerciselist.views',
    (r'^get_code/$', 'get_code'),
    (r'^my_exercise_lists/$', GetStudentsExerciseList.as_view()),
    (r'^exercise_list/(?P<exercise_list_id>\d+)/$', 'exercise_list_new'),
    (r'^exercise_list/add/$', 'exercise_list_add_or_update'),
    (r'^exercise_list/update/([0-9]+)/$', 'exercise_list_add_or_update'),
    (r'^exercise_list/delete/([0-9]+)/$', 'exercise_list_delete'),
    
)
