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
def get_answer_data(answer_id):
    answer = Answer.objects.get(id=answer_id)
    group = answer.exercise_list_solution.get_group()
    answer_text = answer.casted().__unicode__()
    question = answer.question_answered
    form = AnswerCorrectForm(instance=answer, prefix=str(answer.id))
    true_false = answer.casted() in TrueFalseAnswer.objects.all()
    return (group, question, answer_text, form, true_false)

# Save answer in the DB and updates its score
def save_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    form = AnswerCorrectForm(request.POST, instance=answer, prefix=str(answer.id))
    if form.is_valid():
        form.save()
    answer.exercise_list_solution.update_score()

# Viewer for exercise list report
@teacher_required
def exercise_list_correct(request, list_id):
    values = {}
    values['user'] = Profile.objects.get(user=request.user)
    values['exercise_list'] = exercise_list = ExerciseList.objects.get(id=list_id)
    values['exercise_list_score'] = exercise_list.mean()
    through_objects = ExerciseListQuestionThrough.objects.filter(exerciselist=exercise_list)
    values['ordered_questions'] = ordered_questions = [(t.order, t.question) for t in through_objects]
    values['weights'] = [t.weight for t in through_objects]
    students = exercise_list.course.student.all()

    values['student_answers']=[]
    for s in students:
        solution = s.get_group(exercise_list).solution
        solution.populate_blank()
        values['student_answers'].append((s, [solution.answer_set.get(question_answered = q) for (o, q) in ordered_questions], solution.score, solution.finalized))

    values['questions_mean'] = [exercise_list.question_mean(q) for (o, q) in ordered_questions]
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
    if request.method == 'POST':
        for _o, q in ordered_questions:
            save_answer(request, Answer.objects.get(question_answered=q, exercise_list_solution=group.solution).id)
        return HttpResponseRedirect('/exercise_list/correct/' + str(exercise_list.id))

    values['answer_data'] = [get_answer_data(Answer.objects.get(question_answered=q, exercise_list_solution=group.solution).id) for _o, q in ordered_questions]
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
    if request.method == 'POST':
        for a in answers:
            save_answer(request, a.id)
        return HttpResponseRedirect('/exercise_list/correct/' + str(exercise_list.id))
    values['group_answers'] = [get_answer_data(a.id) for a in answers]
    return render_to_response('answer_list.html', values)

# Viewer for a student question correction
@teacher_required
def answer_correct(request, answer_id):
    values = {}
    values.update(csrf(request))
    values['user'] = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        save_answer(request, answer_id)
        exercise_list = Answer.objects.get(id=answer_id).exercise_list_solution.exercise_list
        return HttpResponseRedirect('/exercise_list/correct/' + str(exercise_list.id))
    values['answer_data'] = [get_answer_data(answer_id)]
    return render_to_response('answer_correct.html', values)

# Viewer for questions that haven't been corrected yet:
@teacher_required
def answer_new(request, exercise_list_id):
    values = {}
    values.update(csrf(request))
    values['user'] = Profile.objects.get(user=request.user)
    exercise_list = ExerciseList.objects.get(id=exercise_list_id)
    answers = Answer.objects.filter(score=None, exercise_list_solution__exercise_list=exercise_list)
    if request.method == 'POST':
        for a in answers:
            save_answer(request, a.id)
        return HttpResponseRedirect('/exercise_list/correct/' + str(exercise_list.id))
    values['group_answers'] = [get_answer_data(a.id) for a in answers]
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
        user = Profile.objects.get(user=self.request.user)
        if user.is_student():
            context['student'] = True
        elif user.is_teacher():
            context['teacher'] = True
        context['user'] = user
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
    values['topics'] = topics = exercise_list.topics.all()
    values['chosen_topic'] = None

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
        return HttpResponseRedirect('/exercise_list_solution/' + str(exercise_list_solution.id))
    
    #If the request method is GET, don't pass any data to the forms.
    #Else, pass request.POST.
    if request.method == 'GET':
        data = None
    else:
        data = request.POST

    #Check this exercise list's topics and if the respective list solution has already a chosen topic
    if topics:
        form = TopicsChoiceForm(data=data, instance=exercise_list_solution, prefix='TOPICSFORM')

        if request.method == 'POST':
            if form.is_valid():
                form.save()
        values['topics_form'] = form

    #If this list's solution has already a chosen topic, send it instead, and remove it from the exercise list
    if exercise_list_solution.chosen_topic:
        values['chosen_topic'] = exercise_list_solution.chosen_topic

        if topics:
            exercise_list.topics.remove(exercise_list_solution.chosen_topic)
            exercise_list.save()

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
                        casted_answer.last_submit_success = java_result_success
                        casted_answer.last_submit_message = java_result_message
                        casted_answer.save()
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
        return HttpResponseRedirect('/exercise_list_solution/' + str(exercise_list_solution.id))

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
            if casted_answer.chosen_alternative:
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
    values['chosen_topic'] = exercise_list_solution.chosen_topic

    return render_to_response('view_exercise_list_solution.html', values)

@teacher_required
def create_modify_exercise_list(request, exercise_list_id=None):
    values = {}
    empty_forms = {}
    values.update(csrf(request))
    values['user'] = Profile.objects.get(user=request.user)


    if request.method == "POST":
        data = request.POST
        values['request_post'] = request.POST
    else:
        data = None

    if exercise_list_id is not None:
        exercise_list = get_object_or_404(ExerciseList, pk=exercise_list_id)
    else:
        exercise_list = None


    exercise_list_form = ExerciseListForm(data=data, instance=exercise_list, prefix='EXLIST')
    values['exercise_list_form'] = exercise_list_form

    if request.method=='POST':
        if exercise_list_form.is_valid():
            exercise_list = exercise_list_form.save()

        post_keys = request.POST.keys()
        new_mu_count = int(request.POST['new_mu_count'])
        new_tf_count = int(request.POST['new_tf_count'])
        new_di_count = int(request.POST['new_di_count'])
        new_fi_count = int(request.POST['new_fi_count'])
        new_ja_count = int(request.POST['new_ja_count'])

    else:
        post_keys = []
        new_mu_count = 0
        new_tf_count = 0
        new_di_count = 0
        new_fi_count = 0
        new_ja_count = 0

    #Multiple
    processed_new_mu = 0
    new_mu_index = 1
    while processed_new_mu < new_mu_count:
        if 'new_mu_question-'+unicode(new_mu_index)+'-text' in post_keys:
            new_mu_prefix = 'new_mu_question-'+unicode(new_mu_index)
            new_mu_question_form = MultipleChoiceQuestionForm(data=data, prefix=new_mu_prefix)

            order_form = OrderForm(data=data, prefix=new_mu_prefix+'_ORDER')
            if order_form.is_valid():
                order = order_form.cleaned_data['order']
            else:
                order = 1

            weight_form = WeightForm(data=data, prefix=new_mu_prefix+'_WEIGHT')
            if weight_form.is_valid():
                weight = weight_form.cleaned_data['weight']
            else:
                weight = 1

            if new_mu_question_form.is_valid():
                new_mu_question = new_mu_question_form.save()
                relationship = ExerciseListQuestionThrough(question=new_mu_question, exerciselist=exercise_list, order=order, weight=weight)
                relationship.save()
            processed_new_mu += 1

            #Multiple question, correct item
            new_mu_correct_prefix = new_mu_prefix+'_correct'
            new_mu_correct_form = MultipleChoiceCorrectAlternativeForm(data=data, prefix=new_mu_correct_prefix)
            if new_mu_correct_form.is_valid():
                new_mu_correct = new_mu_correct_form.save(commit=False)
                new_mu_correct.question = new_mu_question
                new_mu_correct.save()

            #Multiple question items
            new_item_count = int(data[new_mu_prefix+'_item_count'])
            for item_number in range(1,new_item_count+1):
                new_item_prefix = 'new_mu_question-'+unicode(new_mu_index)+'_item-'+unicode(item_number)
                new_item_form = MultipleChoiceWrongAlternativeForm(data=data, prefix=new_item_prefix)
                if new_item_form.is_valid():
                    new_item = new_item_form.save(commit=False)
                    new_item.question = new_mu_question
                    new_item.save()

        new_mu_index +=1

    #Discursive
    processed_new_di = 0
    new_di_index = 1
    while processed_new_di < new_di_count:
        if 'new_di_question-'+unicode(new_di_index)+'-text' in post_keys:
            new_di_prefix = 'new_di_question-'+unicode(new_di_index)
            new_di_question_form = DiscursiveQuestionForm(data=data, prefix=new_di_prefix)

            order_form = OrderForm(data=data, prefix=new_di_prefix+'_ORDER')
            if order_form.is_valid():
                order = order_form.cleaned_data['order']
            else:
                order = 1

            weight_form = WeightForm(data=data, prefix=new_di_prefix+'_WEIGHT')
            if weight_form.is_valid():
                weight = weight_form.cleaned_data['weight']
            else:
                weight = 1

            if new_di_question_form.is_valid():
                new_di_question = new_di_question_form.save()
                relationship = ExerciseListQuestionThrough(question=new_di_question, exerciselist=exercise_list, order=order, weight=weight)
                relationship.save()
            processed_new_di += 1
        new_di_index +=1

    #Java
    processed_new_ja = 0
    new_ja_index = 1
    while processed_new_ja < new_ja_count:
        if 'new_ja_question-'+unicode(new_ja_index)+'-text' in post_keys:
            new_ja_prefix = 'new_ja_question-'+unicode(new_ja_index)
            new_ja_question_form = JavaQuestionForm(data=data, prefix=new_ja_prefix)

            order_form = OrderForm(data=data, prefix=new_ja_prefix+'_ORDER')
            if order_form.is_valid():
                order = order_form.cleaned_data['order']
            else:
                order = 1

            weight_form = WeightForm(data=data, prefix=new_ja_prefix+'_WEIGHT')
            if weight_form.is_valid():
                weight = weight_form.cleaned_data['weight']
            else:
                weight = 1

            if new_ja_question_form.is_valid():
                new_ja_question = new_ja_question_form.save()
                relationship = ExerciseListQuestionThrough(question=new_ja_question, exerciselist=exercise_list, order=order, weight=weight)
                relationship.save()
            processed_new_ja += 1
        new_ja_index +=1

    #File
    processed_new_fi = 0
    new_fi_index = 1
    while processed_new_fi < new_fi_count:
        if 'new_fi_question-'+unicode(new_fi_index)+'-text' in post_keys:
            new_fi_prefix = 'new_fi_question-'+unicode(new_fi_index)
            new_fi_question_form = FileQuestionForm(data=data, prefix=new_fi_prefix)

            order_form = OrderForm(data=data, prefix=new_fi_prefix+'_ORDER')
            if order_form.is_valid():
                order = order_form.cleaned_data['order']
            else:
                order = 1

            weight_form = WeightForm(data=data, prefix=new_fi_prefix+'_WEIGHT')
            if weight_form.is_valid():
                weight = weight_form.cleaned_data['weight']
            else:
                weight = 1

            if new_fi_question_form.is_valid():
                new_fi_question = new_fi_question_form.save()
                relationship = ExerciseListQuestionThrough(question=new_fi_question, exerciselist=exercise_list, order=order, weight=weight)
                relationship.save()
            processed_new_fi += 1
        new_fi_index +=1

    #TrueFalse
    processed_new_tf = 0
    new_tf_index = 1
    while processed_new_tf < new_tf_count:
        if 'new_tf_question-'+unicode(new_tf_index)+'-text' in post_keys:
            new_tf_prefix = 'new_tf_question-'+unicode(new_tf_index)
            new_tf_question_form = TrueFalseQuestionForm(data=data, prefix=new_tf_prefix)

            order_form = OrderForm(data=data, prefix=new_tf_prefix+'_ORDER')
            if order_form.is_valid():
                order = order_form.cleaned_data['order']
            else:
                order = 1

            weight_form = WeightForm(data=data, prefix=new_tf_prefix+'_WEIGHT')
            if weight_form.is_valid():
                weight = weight_form.cleaned_data['weight']
            else:
                weight = 1

            if new_tf_question_form.is_valid():
                new_tf_question = new_tf_question_form.save()
                relationship = ExerciseListQuestionThrough(question=new_tf_question, exerciselist=exercise_list, order=order, weight=weight)
                relationship.save()
            processed_new_tf += 1

            #TrueFalse items
            new_item_count = int(data[new_tf_prefix+'_item_count'])
            for item_number in range(1,new_item_count+1):
                new_item_prefix = 'new_tf_question-'+unicode(new_tf_index)+'_item-'+unicode(item_number)
                new_item_form = TrueFalseQuestionItemForm(data=data, prefix=new_item_prefix)
                if new_item_form.is_valid():
                    new_item = new_item_form.save(commit=False)
                    new_item.question = new_tf_question
                    new_item.save()

        new_tf_index +=1

    if exercise_list is not None:
        exercise_list.save()

    #Update old questions or display on GET.
    through_objects = ExerciseListQuestionThrough.objects.filter(exerciselist=exercise_list)
    forms_list = []
    for through_object in through_objects:

        question_form = None
        correct_form = None
        items_forms = []
        casted_question = through_object.question.casted()

        delete_form = DeleteObjectForm(data=request.POST, prefix=str(casted_question.id) + '_DELETE')

        if delete_form.is_valid():
            if delete_form.cleaned_data['delete']:
                through_object.delete()

            else:
                if casted_question.type == 'MU':
                    question_form = MultipleChoiceQuestionForm(data=data, instance=casted_question, prefix =  str(casted_question.id) + '_QUESTIONMU')
                    if question_form.is_valid():
                        question_form.save()
                    correct_form = MultipleChoiceCorrectAlternativeForm(data=data, instance=casted_question.multiplechoicecorrectalternative, prefix=str(casted_question.id)+'-'+str(casted_question.multiplechoicecorrectalternative.id)+'_CORRECTMU')
                    if correct_form.is_valid():
                        correct_form.save()
                    items = casted_question.multiplechoicewrongalternative_set
                    for item in items.all():
                        item_form = MultipleChoiceWrongAlternativeForm(data=data, instance=item, prefix = str(casted_question.id)+'-'+str(item.id)+'_WRONGMU')
                        if item_form.is_valid():
                            item_form.save()
                        items_forms.append(item_form)
                elif casted_question.type == 'DI':
                    question_form = DiscursiveQuestionForm(data=data, instance=casted_question, prefix =  str(casted_question.id) + '_QUESTIONDI')
                    if question_form.is_valid():
                        question_form.save()
                elif casted_question.type == 'JA':
                    question_form = JavaQuestionForm(data=data, instance=casted_question, prefix = str(casted_question.id) + '_QUESTIONJA')
                    if question_form.is_valid():
                        question_form.save()
                elif casted_question.type == 'TF':
                    question_form = TrueFalseQuestionForm(data=data, instance=casted_question, prefix = str(casted_question.id) + '_QUESTIONTF')
                    if question_form.is_valid():
                        question_form.save()
                    items = casted_question.truefalseitem_set
                    for item in items.all():
                        item_form = TrueFalseQuestionItemForm(data=data, instance=item, prefix = str(casted_question.id)+'-'+str(item.id)+'_ITEMTF')
                        if item_form.is_valid():
                            item_form.save()
                        items_forms.append(item_form)
                elif casted_question.type == 'FI':
                    question_form = FileQuestionForm(data=data, instance=casted_question, prefix = str(casted_question.id) + '_QUESTIONFI')
                    if question_form.is_valid():
                        question_form.save()

                #Update order
                order_form = OrderForm(data=request.POST, prefix=str(casted_question.id)+ '_ORDER')
                if order_form.is_valid():
                    through_object.order = order_form.cleaned_data['order']

                #Update weight
                if request.method == 'GET':
                    weight_form = WeightForm(initial = {'weight': through_object.weight}, prefix=str(casted_question.id)+ '_WEIGHT')
                else:
                    weight_form = WeightForm(data=request.POST, prefix=str(casted_question.id) + '_WEIGHT')
                    if weight_form.is_valid():
                        through_object.weight = weight_form.cleaned_data['weight']

                through_object.save()
                forms_list.append({'question_form': question_form, 'order_form': order_form, 'correct_form': correct_form, 'items_forms' : items_forms, 'delete_form' : delete_form, 'order': through_object.order, 'weight_form' : weight_form})

    #Reorder form_list to the new values of order
    forms_list = sorted(forms_list, key=lambda k: k['order'])
    values['form_list'] = forms_list


    #Empty forms generation
    empty_forms['discursive'] = DiscursiveQuestionForm(prefix='__prefix__')

    empty_forms['java'] = JavaQuestionForm(prefix='__prefix__')

    empty_forms['multiple'] = MultipleChoiceQuestionForm(prefix='__prefix__')
    empty_forms['multiple_correct'] = MultipleChoiceCorrectAlternativeForm(prefix='__prefix__')
    empty_forms['multiple_wrong'] = MultipleChoiceWrongAlternativeForm(prefix='__prefix__')

    empty_forms['file'] = FileQuestionForm(prefix='__prefix__')

    empty_forms['truefalse'] = TrueFalseQuestionForm(prefix='__prefix__')
    empty_forms['truefalse_item'] = TrueFalseQuestionItemForm(prefix='__prefix__')
    empty_forms['order'] = OrderForm(prefix='__prefix__')
    empty_forms['weight'] = WeightForm(prefix='__prefix__')

    values['empty_forms'] = empty_forms

    if request.method == 'POST':
        return HttpResponseRedirect('/create_modify_exercise_list'+'/'+str(exercise_list.id))
    else:
        return render_to_response('create_modify_exercise_list.html', values)
