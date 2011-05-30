# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.generic.create_update import create_object, update_object, delete_object
from authentication.models import Profile, Student, Teacher
from authentication.decorators import profile_required, teacher_required
from course.models import Course
from exerciselist.models import * 
from forms import *
from django.forms.models import inlineformset_factory

from django.utils.functional import curry
import os.path, sys
from subprocess import Popen, PIPE
import shlex

from exerciselist.forms import *
@teacher_required
def exercise_list_add_or_update(request, list_id=None):
    if list_id:
        return update_object(request, model=ExerciseList, object_id=list_id, 
                template_name='exercise_list_form.html', post_save_redirect='/')
    else:
        return create_object(request, model=ExerciseList, 
                template_name='exercise_list_form.html', post_save_redirect='/')

@teacher_required
def exercise_list_delete(request, list_id):
    return delete_object(request, model=ExerciseList, object_id=list_id, 
            template_name='exercise_list_confirm_delete.html', post_delete_redirect='/')

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

class GetStudentsExerciseList(ListView):
    context_object_name = 'exercise_list_list'
    template_name = 'students_exercise_lists.html'
    
    def get_queryset(self):
        student = Profile.objects.get(user=self.request.user)

        return ExerciseList.objects.filter(course__student=student) 

    @method_decorator(profile_required)
    def dispatch(self, *args, **kargs):
        return super(GetStudentsExerciseList, self).dispatch(*args, **kargs)


@profile_required
def exercise_list(request, exercise_list_id):
    values = {}
    values.update(csrf(request))
    student = Student.objects.get(user=request.user)
    exercise_list = get_object_or_404(ExerciseList, pk=exercise_list_id)
    course = exercise_list.course
    if not course.has_student(student):
        return HttpResponseRedirect('/')

    #Get or create the exercise list solution and its questions
    exercise_list_solution, exercise_list_solution_created = ExerciseListSolution.objects.get_or_create(student=student, exercise_list=exercise_list)
    exercise_list_solution.populate_blank()

    questions_and_forms = {}
    
    #If the request method is GET, don't pass any data to the forms.
    #Else, pass request.POST.
    if request.method == 'GET':
        data = None
    else:
        data = request.POST

    #For each answer in the exercise list solution, get the filled (bound) form associated with it
    #If the request is of the type POST, it will be filled with the POST DATA
    for answer in exercise_list_solution.answer_set.all():
        casted_answer = answer.casted()
        question_answered = answer.question_answered

        if casted_answer.type == 'MU':
            form = MultipleChoiceAnswerModelForm(data=data, instance=casted_answer, prefix =  str(casted_answer.id) + '_ANSWERMU')
        elif casted_answer.type == 'DI':
            form = DiscursiveAnswerModelForm(data=data, instance=casted_answer, prefix =  str(casted_answer.id) + '_ANSWERDI')
        elif casted_answer.type == 'JA': 
            form = JavaAnswerModelForm(data=data, instance=casted_answer, prefix = str(casted_answer.id) + '_ANSWERJA')
        elif casted_answer.type == 'TF':
            #Check https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#inline-formsets for details on this one
            TrueFalseFormSet = inlineformset_factory(TrueFalseAnswer, TrueFalseAnswerItem, extra=0, can_delete=False, fields=('given_answer',))
            form = TrueFalseFormSet(data=data, instance=casted_answer, prefix = str(casted_answer.id) + '_ANSWERTF')
        
        questions_and_forms[question_answered] = form

        #If the request is a POST, validate each form.
        #If the form is valid, save it.
        if request.method == 'POST':
            if form.is_valid():
                form.save()

    values['questions_and_forms'] = questions_and_forms
    return render_to_response('view_exercise_list.html', values)
