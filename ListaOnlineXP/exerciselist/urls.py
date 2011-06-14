# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from views import GetStudentsExerciseList

urlpatterns = patterns(
    'exerciselist.views',
    (r'^my_exercise_lists/$', GetStudentsExerciseList.as_view()),
    (r'^exercise_list/(?P<exercise_list_id>\d+)/$', 'exercise_list'),
    (r'^exercise_list_solution/(?P<exercise_list_solution_id>\d+)/$', 'view_exercise_list_solution'),
    (r'^exercise_list/add/$', 'exercise_list_add_or_update'),
    (r'^exercise_list/update/([0-9]+)/$', 'exercise_list_add_or_update'),
    (r'^exercise_list/delete/([0-9]+)/$', 'exercise_list_delete'),
    (r'^create_modify_exercise_list/$', 'create_modify_exercise_list'),
    (r'^create_modify_exercise_list/(?P<exercise_list_id>\d+)/$', 'create_modify_exercise_list'),
    
)
