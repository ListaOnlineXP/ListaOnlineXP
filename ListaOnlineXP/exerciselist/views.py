# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.generic.create_update import create_object, update_object, delete_object
from authentication.models import *
from authentication.decorators import profile_required, teacher_required
from course.models import Course
from exerciselist.models import * 
from forms import *
from django.forms.models import inlineformset_factory

from exerciselist.forms import *

from utilities import test_code

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
    
    print student.name
    print exercise_list.name

    course = exercise_list.course
    if not course.has_student(student):
        return HttpResponseRedirect('/')
    
    group = student.get_group(exercise_list)

    if group is None:
        return HttpResponseRedirect('/groups/' + str(exercise_list.id))

    #Get or create the exercise list solution and its questions
    exercise_list_solution = group.solution
    exercise_list_solution.populate_blank()

    
    #If the request method is GET, don't pass any data to the forms.
    #Else, pass request.POST.
    if request.method == 'GET':
        data = None
    else:
        data = request.POST

    questions_and_forms_list = []

    #For each answer in the exercise list solution, get the filled (bound) form associated with it
    #If the request is of the type POST, it will be filled with the POST DATA


    for through_object in ExerciseListQuestionThrough.objects.filter(exerciselist=exercise_list_solution.exercise_list):
        question_answered = through_object.question
        casted_answer = exercise_list_solution.answer_set.get(question_answered = question_answered).casted()
        java_result = None


        if casted_answer.type == 'MU':
            form = MultipleChoiceAnswerForm(data=data, instance=casted_answer, prefix =  str(casted_answer.id) + '_ANSWERMU')
        elif casted_answer.type == 'DI':
            form = DiscursiveAnswerForm(data=data, instance=casted_answer, prefix =  str(casted_answer.id) + '_ANSWERDI')
        elif casted_answer.type == 'JA':
            form = JavaAnswerForm(data=data, instance=casted_answer, prefix = str(casted_answer.id) + '_ANSWERJA')

            #Test java code, save the result
            if request.method == 'POST':
                code_in_database = casted_answer.code
                if form.is_valid():
                    code = form.cleaned_data['code']
                    test = question_answered.casted().criteria
                    #Only re-test if the submitted code is different from what was already in the database
                    #Testing is an expensive operation.
                    if not code == code_in_database:
                        java_result_success, java_result_message = test_code(test=test, code=code)
                        casted_answer.last_submit_result = java_result_success
                        casted_answer.last_submit_message = java_result_message
            java_result = casted_answer.last_submit_message

        elif casted_answer.type == 'TF':
            #Check https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#inline-formsets for details on this one
            TrueFalseFormSet = inlineformset_factory(TrueFalseAnswer, TrueFalseAnswerItem, form =TrueFalseAnswerItemForm, extra=0, can_delete=False, fields=('given_answer',))
            form = TrueFalseFormSet(data=data, instance=casted_answer, prefix = str(casted_answer.id) + '_ANSWERTF')
        elif casted_answer.type == 'FI':
            form = FileAnswerForm(data=data, files=request.FILES, instance=casted_answer, prefix = str(casted_answer.id) + '_ANSWERFI')

        questions_and_forms_list.append({'question' : question_answered, 'form' : form, 'java_result' : java_result})

        #If the request is a POST, validate each form.
        #If the form is valid, save it.
        if request.method == 'POST':
            if form.is_valid():
                form.save()
    
    #If the solution is finalized, correct the answers
    if request.method == 'POST' and 'finalize' in request.POST:
        exercise_list_solution.correct()
        values['score'] = exercise_list_solution.score
        exercise_list_solution.finalized = True

    #If for test and debug
    if request.method == 'POST' and 'rollback' in request.POST:
        exercise_list_solution.finalized = False

    values['finalized'] = exercise_list_solution.finalized
    values['questions_and_forms_list'] = questions_and_forms_list
    values['user'] = student
    return render_to_response('view_exercise_list.html', values)

@profile_required
def view_exercise_list_solution(request, exercise_list_solution_id):
    values = {}
    questions_answers_list = []
    student = Student.objects.get(user=request.user)
    exercise_list_solution = ExerciseListSolution.objects.get(pk=exercise_list_solution_id)
    course = exercise_list_solution.exercise_list.course

    if not course.has_student(student):
        return HttpResponseRedirect('/')
    
    for through_object in ExerciseListQuestionThrough.objects.filter(exerciselist=exercise_list_solution.exercise_list):
        question_answered = through_object.question
        casted_answer = exercise_list_solution.answer_set.get(question_answered = question_answered).casted()
        
        if casted_answer.type == 'FI':
            given_answer = casted_answer.file.url
        elif casted_answer.type == 'MU':
            given_answer = casted_answer.chosen_alternative.text
        elif casted_answer.type == 'DI':
            given_answer = casted_answer.text
        elif casted_answer.type == 'JA':
            given_answer = casted_answer.code
        elif casted_answer.type == 'TF':
            #TODO: Work a little more on this one: not very pretty, just text, and it includes formatting in the view. The template should be in charge of formatting.
            given_answer = ''
            for answer_item in casted_answer.truefalseansweritem_set.all():
                given_answer += answer_item.item_answered.text + ': ' +str(answer_item.given_answer)  + '\n'
        else:
            given_answer = None
            

        question_answer = {'question' : question_answered, 'answer' : given_answer}
        questions_answers_list.append(question_answer)

    values['questions_answers_list'] = questions_answers_list
    values['student_name'] = student.name
    values['exercise_list_title'] = exercise_list_solution.exercise_list.name
    return render_to_response('view_exercise_list_solution.html', values)



