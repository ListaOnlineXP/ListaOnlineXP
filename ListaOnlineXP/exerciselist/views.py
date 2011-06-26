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


#===Begin viewer for Correction===
# Returns a tuple with the information of the given answer to help the
# construction of correction views
# tuple = (owner group, question, answer given, form for correction, 
#         trueFalse question?)
def get_answer_data(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    group = answer.exercise_list_solution.get_group()
    answer_text = answer.casted().__unicode__()
    question = answer.question_answered
    if request.method == 'POST':
        form = AnswerCorrectForm(request.POST, instance=answer, prefix=str(answer.id))
        if form.is_valid():
            form.save()
        answer.exercise_list_solution.update_score()
    else:
        form = AnswerCorrectForm(instance=answer, prefix=str(answer.id))
    true_false = answer.casted() in TrueFalseAnswer.objects.all()
    return (group, question, answer_text, form, true_false)

# Viewer for exercise list report
@teacher_required
def exercise_list_correct(request, list_id):
    values = {}
    values['user'] = Profile.objects.get(user=request.user)
    values['exercise_list'] = exercise_list = ExerciseList.objects.get(id=list_id)
    through_objects = ExerciseListQuestionThrough.objects.filter(exerciselist=exercise_list)
    values['ordered_questions'] = [(t.order, t.question) for t in through_objects]
    values['weights'] = [t.weight for t in through_objects]
    students = exercise_list.course.student.all()
    values['student_answers'] = [(s, [s.get_group(exercise_list).solution.answer_set.get(question_answered = q) for (o, q) in values['ordered_questions']], s.get_group(exercise_list).solution.score) for s in students]
        
    return render_to_response('question_list.html', values)

# Viewer for student exercise list correction
@teacher_required
def answer_student(request, student_id, list_id):
    values = {}
    values.update(csrf(request))
    values['user'] = Profile.objects.get(user=request.user)
    values['exercise_list'] = exercise_list = ExerciseList.objects.get(id=list_id)
    values['group'] = group = Student.objects.get(id=student_id).get_group(exercise_list)
    ordered_questions = [(t.order, t.question) for t in ExerciseListQuestionThrough.objects.filter(exerciselist=exercise_list)]
    values['answer_data'] = [get_answer_data(request, Answer.objects.get(question_answered=q, exercise_list_solution=group.solution).id) for _o, q in ordered_questions]

    if request.method == 'POST':
        return HttpResponseRedirect('/exercise_list/correct/' + str(exercise_list.id))
    return render_to_response('answer_correct.html', values)

# Viewer for a question correction
@teacher_required
def answer_list(request, question_id, exercise_list_id):
    values = {}
    values.update(csrf(request))
    values['user'] = Profile.objects.get(user=request.user)
    values['question'] = question = Question.objects.get(id=question_id)
    exercise_list = ExerciseList.objects.get(id=exercise_list_id)
    answers = []
    for solution in ExerciseListSolution.objects.filter(exercise_list=exercise_list):
	answers.append(Answer.objects.get(question_answered=question, exercise_list_solution=solution))
    values['group_answers'] = [get_answer_data(request, a.id) for a in answers]
    if request.method == 'POST':
        return HttpResponseRedirect('/exercise_list/correct/' + str(exercise_list.id))
    return render_to_response('answer_list.html', values)

# Viewer for a student question correction
@teacher_required
def answer_correct(request, answer_id):
    values = {}
    values.update(csrf(request))
    values['user'] = Profile.objects.get(user=request.user)
    values['answer_data'] = [get_answer_data(request, answer_id)]
    if request.method == 'POST':
        exercise_list = Answer.objects.get(id=answer_id).exercise_list_solution.exercise_list
        return HttpResponseRedirect('/exercise_list/correct/' + str(exercise_list.id))
    return render_to_response('answer_correct.html', values)

# Viewer for questions that haven't been corrected ye:
@teacher_required
def answer_new(request, exercise_list_id):
    values = {}
    values.update(csrf(request))
    values['user'] = Profile.objects.get(user=request.user)
    exercise_list = ExerciseList.objects.get(id=exercise_list_id)
    answers = Answer.objects.filter(score=None, exercise_list_solution__exercise_list=exercise_list)
    values['group_answers'] = [get_answer_data(request, a.id) for a in answers]
    if request.method == 'POST':
        return HttpResponseRedirect('/exercise_list/correct/' + str(exercise_list.id))
    return render_to_response('answer_new.html', values)
#===End viewer for correction===

class GetMyExerciseList(ListView):
    context_object_name = 'exercise_list_list'
    template_name = 'my_exercise_lists.html'

    def get_queryset(self):
        user = Profile.objects.get(user=self.request.user)
        if user.is_student():
            return ExerciseList.objects.filter(course__student=user) 
        else:
            return ExerciseList.objects.filter(course__teacher=user) 

    def get_context_data(self, **kargs):
        context = super(GetMyExerciseList, self).get_context_data(**kargs)
        context['user'] = Profile.objects.get(user=self.request.user)
        return context

    @method_decorator(profile_required)
    def dispatch(self, *args, **kwargs):
        return super(GetMyExerciseList, self).dispatch(*args, **kwargs)


@profile_required
def exercise_list(request, exercise_list_id):
    values = {}
    values.update(csrf(request))
    values['user'] = user = Profile.objects.get(user=request.user)
    exercise_list = get_object_or_404(ExerciseList, pk=exercise_list_id)

    if not user.is_student():
        return HttpResponseRedirect('/exercise_list/correct/' + str(exercise_list.id))

    student = user.student
    
    course = exercise_list.course
    if not course.has_student(student):
        return HttpResponseRedirect('/')
    
    group = student.get_group(exercise_list)

    if group is None:
        return HttpResponseRedirect('/groups/' + str(exercise_list.id))

    #Get or create the exercise list solution and its questions
    exercise_list_solution = group.solution
    exercise_list_solution.populate_blank()

    if exercise_list_solution.finalized is True:
        return HttpResponseRedirect('/exercise_list_solution/' + str(exercise_list_id))
    
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
        exercise_list_solution.save()
        return HttpResponseRedirect('/exercise_list_solution/' + str(exercise_list_id))

    exercise_list_solution.save()
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
        
        given_answer = ''
        if casted_answer.type == 'FI': 
            if not casted_answer.file == '':
                given_answer = casted_answer.file.url
        elif casted_answer.type == 'MU':
            given_answer = casted_answer.chosen_alternative.text
        elif casted_answer.type == 'DI':
            given_answer = casted_answer.text
        elif casted_answer.type == 'JA':
            given_answer = casted_answer.code
        elif casted_answer.type == 'TF':
            #TODO: Work a little more on this one: not very pretty, just text, and it includes formatting in the view. The template should be in charge of formatting.
            for answer_item in casted_answer.truefalseansweritem_set.all():
                given_answer += answer_item.item_answered.text + ': ' +str(answer_item.given_answer)  + '\n'
        else:
            given_answer = None

        question_answer = {'question' : question_answered, 'answer' : given_answer,
                'score': casted_answer.score, 'comment': casted_answer.comment}
        questions_answers_list.append(question_answer)

    values['user'] = Profile.objects.get(user=request.user)
    values['questions_answers_list'] = questions_answers_list
    values['student_name'] = student.name
    values['exercise_list_title'] = exercise_list_solution.exercise_list.name
    return render_to_response('view_exercise_list_solution.html', values)

@teacher_required
def create_modify_exercise_list(request, exercise_list_id=None):
    values = {}
    empty_forms = {}
    values.update(csrf(request))

    if request.method == 'POST':

        values['POST_print'] = ""
        for key, value in request.POST.iteritems():
            #Debug
            values['POST_print'] += 'Chave: ' + unicode(key) + '\tValor: ' + unicode(value) + '\n'
            #Debug

            post_keys = request.POST.keys()
            if 'new_tf_question' in str(post_keys):
                
                pass

#            if "new_tf_question" in key:
#
#                pass
#            elif "new_mu_question" in key:
#                if "item" not in key:
#                    form = MultipleChoiceQuestionForm(data = {})
#                else:
#                    if "correct" in key:
#                        form = MultipleChoiceCorrectAlternativeForm(data = {})
#                    elif "wrong" in key:
#                        form = MultipleChoiceWrongAlternativeForm(data = {})
#                    else:
#                        print("Valor não esperado: " + key)
#                pass
#            elif "new_fi_question" in key:
#                form = FileQuestionForm(data={})
#                pass
#            elif "new_ja_question" in key:
#                form = JavaQuestionForm(data={})
#                pass
#            elif "new_di_question" in key:
#                form = DiscursiveQuestionForm(data={})
#                pass
#            else:
#                print("Valor não esperado: " + key)





    pass


    if exercise_list_id is None:
        empty_forms['discursive'] = DiscursiveQuestionForm(prefix='__prefix__')

        empty_forms['java'] = JavaQuestionForm(prefix='__prefix__')

        empty_forms['multiple'] = MultipleChoiceQuestionForm(prefix='__prefix__')
        empty_forms['multiple_correct'] = MultipleChoiceCorrectAlternativeForm(prefix='__prefix__')
        empty_forms['multiple_wrong'] = MultipleChoiceWrongAlternativeForm(prefix='__prefix__')

        empty_forms['file'] = FileQuestionForm(prefix='__prefix__')

        empty_forms['truefalse'] = TrueFalseQuestionForm(prefix='__prefix__')
        empty_forms['truefalse_item'] = TrueFalseQuestionItemForm(prefix='__prefix__')


    values['empty_forms'] = empty_forms
    return render_to_response('create_modify_exercise_list.html', values)
