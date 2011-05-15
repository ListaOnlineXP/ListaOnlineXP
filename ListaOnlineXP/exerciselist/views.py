# -*- coding: utf-8 -*-

import shlex
import sys
import os.path
from subprocess import Popen, PIPE
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from authentication.models import Profile
from course.models import Course, CourseMember
from exerciselist.models import ExerciseList, Question, MultipleChoiceQuestion, ExerciseListSolution
from views import *
from forms import *
from authentication.decorators import profile_required


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

@profile_required
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
            student = request.user.get_profile()
            values['student'] = student
            values['exercise_list'] = exercise_list
            values['questions_alternatives'] = exercise_list.get_questions_alternatives() 
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
        student = self.request.user.get_profile()

        return ExerciseList.objects.filter(course__student=student) 

    @method_decorator(profile_required)
    def dispatch(self, *args, **kargs):
        return super(GetStudentsExerciseList, self).dispatch(*args, **kargs)

@profile_required
def view_exercise_list(request, exercise_list_id):
    values = {}
    values.update(csrf(request))
    student = request.user.get_profile()
    values['student'] = student
    exercise_list = get_object_or_404(ExerciseList, pk=exercise_list_id)
    course = exercise_list.course
    if not CourseMember.is_member_of_course(student, course):
        return HttpResponseRedirect('/')

    #Here, we have the student, the exercise_list and the course.
    #We have also verified that the student is enrolled in the
    #course, so the basic checks are done and we're ready to roll.

    if request.method == 'GET':
        #Get the multiple choice questions associated with this exercise list. The exercise list has a method that returns its multiple choice questions as a queryset.
        multiple_choice_questions = exercise_list.get_multiple_choice_questions()

        #Initialize a dictionary which will hold questions and its form. The question will act as the key for the dictionary, while the form will act as the value for a particular key(question).
        questions_and_forms = {}
        #Start populating the questions_and_forms with multiple_choice_question as keys, MultipleChoiceQuestionForm as the value. Add a prefix to each form so they don't collide.
        for multiple_choice_question in multiple_choice_questions:
            questions_and_forms[multiple_choice_question] = MultipleChoiceQuestionForm(multiple_choice_question=multiple_choice_question, prefix=multiple_choice_question.pk)

        #Once the dictionary is populated, send it to the values dictionary (a dictionary inside a dictionary works fine in the template, and is very useful)
        
        #The same thing for java questions, except its form is simpler:
        java_questions = exercise_list.get_java_questions()
        for java_question in java_questions:
            questions_and_forms[java_question] = JavaQuestionForm(prefix=java_question.pk)
        
        discursive_questions = exercise_list.get_discursive_questions()
        for discursive_question in discursive_questions:
            questions_and_forms[discursive_question] = DiscursiveQuestionForm(prefix = discursive_question.pk)
        
        values['questions_and_forms'] =  questions_and_forms

        

    if request.method == 'POST':
        pass
    #End Multiple Choice section
    
    

    return render_to_response('view_exercise_list.html', values)

    
@profile_required    
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
            student = request.user.get_profile()
            admin = get_admin(request)
            values["java_questions"] = JavaQuestions.objects.filter(exerciselist=exercise_list)
        else:
            return HttpResponseRedirect('/')   
    raise Http404
