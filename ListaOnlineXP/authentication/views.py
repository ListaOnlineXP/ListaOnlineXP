# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from forms import SignUpForm, LoginForm
from models import Student


def get_student(request):
    if request.user.is_authenticated():
        try:
            student = Student.objects.get(user=request.user)
            if student is not None:
                return student
        except:
            return None
    return None

def get_admin(request):
    if request.user.is_authenticated() and request.user.is_staff:
        return request.user
    return None

def home(request):
    if get_student(request) is not None:
        return HttpResponseRedirect('/course')
    return HttpResponseRedirect('/login')


def signup(request):
    if get_student(request) is not None:
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

