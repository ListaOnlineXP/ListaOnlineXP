# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User, Group
from forms import SignUpForm, LoginForm
from models import Profile


def login(request):
    values = {}
    values.update(csrf(request))
    next = request.GET.get('next', '/')
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            passwd = form.cleaned_data['passwd']
            user = auth.authenticate(username=username, password=passwd)
            auth.login(request, user)
            return HttpResponseRedirect(next)
    values['form'] = form
    values['next'] = next
    return render_to_response('login.html', values)

def signup(request):
    values = {}
    values['title'] = 'Cadastro de aluno'
    values['user'] = request.user if request.user.is_authenticated() else None
    values.update(csrf(request))
    if request.method == 'GET':
        form = SignUpForm()
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            passwd = form.cleaned_data['passwd']
            try:
                user = User.objects.create_user(username, email, passwd)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                profile = Profile(user=user)
                profile.save()
                auth.login(
                    request,
                    auth.authenticate(
                        username=username,
                        password=passwd
                    )
                )
                return HttpResponseRedirect('/')
            except:
                form._errors['username'] = form.error_class(
                    ['Usuário já cadastrado.']
                )
    values['form'] = form
    return render_to_response('signup.html', values)
