from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from forms import GetCodeForm
from django.views.generic import ListView

from course.models import Course
from exerciselist.models import ExerciseList, MultipleChoiceCorrectAnswer, MultipleChoiceWrongAnswer, MultipleChoiceQuestion
from views import *

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import itertools, random

import os.path
from subprocess import Popen, PIPE
import shlex

from authentication.views import get_student, get_admin

def get_code(request):
    values = {}
    values.update(csrf(request))
    if request.method == 'GET':
        form = GetCodeForm()
    else:
        form = GetCodeForm(request.POST)
        if form.is_valid():

            code_file = open("/Users/hugo/ListaOnlineXP/ListaOnlineXP/java/Code.java", 'w')
            code_file.write(request.POST['code'])
            code_file.close()

            test_file = open("/Users/hugo/ListaOnlineXP/ListaOnlineXP/java/TestCode.java", 'w')
            test_file.write(request.POST['test'])
            test_file.close()

            path = "/Users/hugo/ListaOnlineXP/ListaOnlineXP/java/"

            test_command = "java -Dfile.encoding=utf-8 -classpath " + path +  " JavaTester  /Users/hugo/ListaOnlineXP/ListaOnlineXP/java/Code.java /Users/hugo/ListaOnlineXP/ListaOnlineXP/java/TestCode.java " + path

            test_args = shlex.split(test_command)

            test = Popen(test_args, stdout=PIPE, stderr=PIPE)
            test_output = test.stdout.read()

            values["test_output"] = test_output
            values["test_command"] = test_command

    values['form'] = form
    return render_to_response('get_code.html', values)


class GetStudentsExerciseList(ListView):
    context_object_name = 'exercise_list_list'
    template_name = 'students_exercise_lists.html'
    
    def get_queryset(self):
        student = get_student(self.request)

        return ExerciseList.objects.filter(course__student=student) 

    @method_decorator(login_required)
    def dispatch(self, *args, **kargs):
        return super(GetStudentsExerciseList, self).dispatch(*args, **kargs)

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
            student = get_student(request)
            admin = get_admin(request)
            course = exercise_list.course
            questions = list(exercise_list.questions.all())
            answers = []
            for question in questions:
                question_answers = list(MultipleChoiceCorrectAnswer.objects.filter(question=question))
                question_answers.extend(MultipleChoiceWrongAnswer.objects.filter(question=question))
                random.shuffle(question_answers)
                answers.append(question_answers)
            print answers

            values['exercise_list'] = exercise_list
            values['questions'] = itertools.izip(questions, answers)
            values['student'] = student
            if student is not None:
                if course in student.courses.all():
                    return render_to_response('exercise_list.html', values)
                else:
                    return HttpResponseRedirect('/')                
            else:
                return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/')   
    raise Http404            
