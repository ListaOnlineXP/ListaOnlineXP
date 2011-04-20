# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from forms import SignUpForm, LoginForm, GetCodeForm
from models import Student, Teacher, Course

import os.path
from subprocess import Popen, PIPE
import shlex

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

def login(request):
    if get_student(request) is not None:
        return HttpResponseRedirect('/')
    values = {}
    values.update(csrf(request))
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            passwd = form.cleaned_data['passwd']
            try:
                user = User.objects.get(username=username)
                if user.check_password(passwd):
                    user = auth.authenticate(username=username, password=passwd)
                    auth.login(request, user)
                    return HttpResponseRedirect('/course')
                else:
                    form._errors['passwd'] = form.error_class(['Senha incorreta.'])
            except:
                form._errors['username'] = form.error_class(['Usuário não cadastrado.'])
    values['form'] = form
    return render_to_response('login.html', values)

def logout(request):
    if get_student(request) is not None:
        auth.logout(request)
    return HttpResponseRedirect('/')

def course(request, course_id):
    values = {}
    values.update(csrf(request))
    try:
        course = Course.objects.get(id=int(course_id))
    except:
        raise Http404
    if course is not None:
        student = get_student(request)
        admin = get_admin(request)
        values['course'] = course
        if student is not None:
            if course in student.courses.all():
                subscribe = False
            else:
                subscribe = True
            values['subscribe'] = subscribe
            if request.method == 'POST':
                student.courses.add(course)
                student.save()
                return HttpResponseRedirect('/')
            else:
                return render_to_response('course.html', values)
        elif admin is not None:
            values['students'] = course.student_set.all()
            return render_to_response('teacher_course.html', values)
        else:
            return HttpResponseRedirect('/login')
    raise Http404

def course_list(request):
    if get_student(request) is None:
        return HttpResponseRedirect('/')
    student = Student.objects.get(user=request.user)
    course_list = list(Course.objects.all())
    return render_to_response('course_list.html', {'course_list':  course_list, 'student': student})

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
