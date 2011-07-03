# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list

from forms import SignUpForm, LoginForm
from models import Student, Group
from exerciselist.models import ExerciseList
from decorators import profile_required, student_required

@profile_required
def home(request):
    return HttpResponseRedirect('/course')

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    values = {}
    values.update(csrf(request))
    if request.method == 'GET':
        form = SignUpForm()
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            nusp = form.cleaned_data['nusp']
            passwd = form.cleaned_data['passwd']
            try:
                user = User.objects.create_user(username, '', passwd)
                student = Student(name=name, nusp=nusp, user=user)
                student.save()
                return HttpResponseRedirect('/login')
            except:
                form._errors["username"] = form.error_class(["Usuário já cadastrado."])
    values['form'] = form
    return render_to_response('signup.html', values)

@student_required
def groups(request, exercise_list_id):
    values = {}
    values['user'] = student = Student.objects.get(user=request.user)
    values['exercise_list'] = exercise_list = ExerciseList.objects.get(pk=exercise_list_id)
    group_list = Group.objects.filter(solution__exercise_list=exercise_list)

    return object_list(request, queryset=group_list, template_object_name='group', 
            template_name='group_list.html', extra_context=values)

@student_required
def group_update(request, group_id):
    student = Student.objects.get(user=request.user)
    group = Group.objects.get(pk=group_id)
    group.students.add(student)
    
    return HttpResponseRedirect('/exercise_list/'+str(group.solution.exercise_list.pk))
