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
from views import *

from django.forms.models import modelformset_factory


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
def exercise_list_new(request, exercise_list_id):
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

    if request.method == 'GET'

        for question in exercise_list.questions
            given_answer = exercise_list_solutions.answers.objects.get(question_answered=question)
            given_answer = given_answer.casted()

            if given_answer.type == 'JA' or given_answer.type == 'DI':
                questions_and_forms[question] = given_answer.get_form()


    values['questions_and_forms'] = questions_and_forms
    return render_to_response('view_exercise_list.html', values)

        
        




@profile_required
def exercise_list(request, exercise_list_id):
    values = {}
    values.update(csrf(request))
    values['user'] = student = Student.objects.get(user=request.user)
    exercise_list = get_object_or_404(ExerciseList, pk=exercise_list_id)
    course = exercise_list.course
    if not course.has_student(student):
        return HttpResponseRedirect('/')

    #Here, we have the student, the exercise_list and the course.
    #We have also verified that the student is enrolled in the
    #course, so the basic checks are done and we're ready to roll.

    #Get questions associated with this exercise list.
    #The exercise list has a method that returns each type of question as a queryset.
    multiple_choice_questions = exercise_list.get_multiple_choice_questions()
    java_questions = exercise_list.get_java_questions()
    discursive_questions = exercise_list.get_discursive_questions()

    questions_and_forms = {}
    answers = {}
    default_values = {}

    if request.method == 'GET':
        exercise_list_solution, _created = ExerciseListSolution.objects.get_or_create(student=student, exercise_list=exercise_list)
        exercise_list_solution.populate_blank()
        '''
        If there's a solution in the db, the next lines get the answers and put them in the default_values of the forms.
        The keys of the dictionary default_values are set as: question_id-question_type (ex: '1-alternative')
        Types are: alternative, java_answer and discursive_answer.
        '''

        ''' WIP
        for question in exercise_list.questions.all():
            question = question.casted()
            answer = exercise_list_solution.answers.objects.get(question_answered=question)
            answer =  answer.casted()
            answer.get_form()
        '''

        for question in exercise_list.get_multiple_choice_questions().all():
            answer = MultipleChoiceQuestionAnswer.objects.get(exercise_list_solution=exercise_list_solution, question_answered=question)
            if answer.chosen_alternative:
                default_values[question.id.__str__()+'-alternative'] = answer.chosen_alternative.id
        for question in exercise_list.get_java_questions():
            answer = JavaQuestionAnswer.objects.get(exercise_list_solution=exercise_list_solution, question_answered=question)
            default_values[question.id.__str__()+'-java_answer'] = answer.code
        for question in exercise_list.get_discursive_questions():
            answer = DiscursiveQuestionAnswer.objects.get(exercise_list_solution=exercise_list_solution, question_answered=question)
            default_values[question.id.__str__()+'-discursive_answer'] = answer.text
 
    if request.method == 'POST':
        default_values = request.POST
        exercise_list_solution, solution_created = ExerciseListSolution.objects.get_or_create(student=student, exercise_list=exercise_list)
        
        # get the answers posted in the forms
        for key, value in request.POST.iteritems():
            # ignore keys that are not answers
            try:
                pk = int(key.split('-')[0]) # get question primary key
            except:
                continue
            if 'alternative' in key:
                question = MultipleChoiceQuestion.objects.get(pk=pk)
                alternative = MultipleChoiceAlternative.objects.get(pk=value)
                answers[question] = MultipleChoiceQuestionAnswer.objects.get(exercise_list_solution=exercise_list_solution, question_answered=question)
                answers[question].chosen_alternative = alternative
            elif 'java' in key:
                question = JavaQuestion.objects.get(pk=pk)
                answers[question] = JavaQuestionAnswer.objects.get(exercise_list_solution=exercise_list_solution, question_answered=question) 
                answers[question].code = value
            elif 'discursive' in key:
                question = DiscursiveQuestion.objects.get(pk=pk)
                answers[question] = DiscursiveQuestionAnswer.objects.get(exercise_list_solution=exercise_list_solution, question_answered=question)
                answers[question].text = value

    # instantiating the forms
    if (exercise_list_solution and exercise_list_solution.finalized) or 'finalize' in request.POST:
        values['finalized'] = True
    else:
        values['finalized'] = False
    
    for multiple_choice_question in multiple_choice_questions:
        questions_and_forms[multiple_choice_question] = MultipleChoiceQuestionForm(default_values, multiple_choice_question=multiple_choice_question, prefix=multiple_choice_question.pk, finalized=values['finalized'])
    for java_question in java_questions:
        questions_and_forms[java_question] = JavaQuestionForm(default_values, prefix=java_question.pk, finalized=values['finalized'])
    for discursive_question in discursive_questions:
        questions_and_forms[discursive_question] = DiscursiveQuestionForm(default_values, prefix = discursive_question.pk, finalized=values['finalized'])

    submit = None
    if 'save' in request.POST:
        submit = 'save'
#    elif 'test' in request.POST:
#        submit = 'test'
    elif 'finalize' in request.POST:
        submit = 'finalize'

    # if all forms are valid save the answers.
    if request.method=='POST':
        if submit == 'save':
            for question, form in questions_and_forms.iteritems():
                if form.is_valid():
                    answer[question].save()
            if solution_created:
                exercise_list_solution.save()
#        elif submit == 'test':
            #TODO
        elif submit == 'finalize' and all([form.is_valid() for _question, form in questions_and_forms.iteritems()]):
            for _question, answer in answers.iteritems():
                answer.save()
            values['finalized'] = exercise_list_solution.finalized = True
            exercise_list_solution.save()

    #Once the dictionary is populated, send it to the values dictionary 
    #(a dictionary inside a dictionary works fine in the template, and is very useful)
    values['questions_and_forms'] =  questions_and_forms

    return render_to_response('view_exercise_list.html', values)
   
    
