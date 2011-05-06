# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from forms import GetCodeForm, MultipleChoiceQuestionAnswersForm
from django.views.generic import ListView

from authentication.models import Student
from course.models import Course
from exerciselist.models import ExerciseList, Question, MultipleChoiceQuestion
from views import *

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from itertools import izip
from random import shuffle

import os.path, sys
from subprocess import Popen, PIPE
import shlex


def get_code(request):
    values = {}
    values.update(csrf(request))
    if request.method == 'GET':
        form = GetCodeForm()
    else:
        form = GetCodeForm(request.POST)
        if form.is_valid():
            path = os.path.dirname(__file__) + "/java/"
            
            print path

            code_file = open(path + "Code.java", 'w')
            code_file.write(request.POST['code'])
            code_file.close()

            test_file = open(path + "TestCode.java", 'w')
            test_file.write(request.POST['test'])
            test_file.close()

            test_command = "java -Dfile.encoding=utf-8 -classpath " + path +  " JavaTester  " + path + "Code.java " + path + "TestCode.java " + path

            test_args = shlex.split(test_command)

            test = Popen(test_args, stdout=PIPE, stderr=PIPE)
            test_output = test.stdout.read()

            values["test_output"] = test_output
            values["test_command"] = test_command

    values['form'] = form
    return render_to_response('get_code.html', values)

# auxiliar method
def get_questions_alternatives(exercise_list):
    questions = exercise_list.questions.all()
    alternatives = []
    for question in questions:
        multiple_choice_question = MultipleChoiceQuestion.objects.get(pk=question.pk)
        alternatives.append(list(multiple_choice_question.get_alternatives()))
    return izip(questions, alternatives)

@login_required
def exercise_list(request, course_id, list_id):
    values = {}
    values.update(csrf(request))
    try:
        course = Course.objects.get(id=int(course_id))
        exercise_list = ExerciseList.objects.get(id=int(list_id))
    except:
        raise Http404
    if (exercise_list is not None) and (course is not None):
        if (exercise_list.course == course):
            student = Student.objects.get(user=request.user)
            values['student'] = student
            values['exercise_list'] = exercise_list
            values['questions_alternatives'] = get_questions_alternatives(exercise_list) 
            if student.is_enrolled(course):
                return render_to_response('exercise_list.html', values)
            else:
                return HttpResponseRedirect('/')                
        else:
            return HttpResponseRedirect('/')   
    raise Http404            


class GetStudentsExerciseList(ListView):
    context_object_name = 'exercise_list_list'
    template_name = 'students_exercise_lists.html'
    
    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)

        return ExerciseList.objects.filter(course__student=student) 

    @method_decorator(login_required)
    def dispatch(self, *args, **kargs):
        return super(GetStudentsExerciseList, self).dispatch(*args, **kargs)
    
    
@login_required    
def view_java_questions(request, exercise_list_id):
    values = {}
    values.update(csrf(request))
    try:
        exercise_list = ExerciseList.objects.get(id=int(exercise_list_id))
        course = exercise_list.course
    except:
        raise Http404
    if (exercise_list is not None) and (course is not None):
        if (exercise_list.course == course):
            student = Student.objects.get(user=request.user) 
            admin = get_admin(request)
            values["java_questions"] = JavaQuestions.objects.filter(exerciselist=exercise_list)
        else:
            return HttpResponseRedirect('/')   
    raise Http404



