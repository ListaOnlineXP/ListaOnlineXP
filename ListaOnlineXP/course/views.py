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

def home(request):
	if request.user.is_authenticated():
		try:
			student = Student.objects.get(user=request.user)
			if student is not None:
				return render_to_response('student.html', {'student': student})
		except:
			return HttpResponseRedirect('/admin/')
	return render_to_response('home.html')

def signup(request):
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
				return HttpResponseRedirect('/login/')
			except:
				form._errors["username"] = form.error_class(["Usuário já cadastrado."])
	values['form'] = form
	return render_to_response('signup.html', values)

def login(request):
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
					return HttpResponseRedirect('/')
				else:
					form._errors['passwd'] = form.error_class(['Senha incorreta.'])
			except:
				form._errors['username'] = form.error_class(['Usuário não cadastrado.'])
	values['form'] = form
	return render_to_response('login.html', values)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def course(request, course_id):
	values = {}
	values.update(csrf(request))
	try:
		course = Course.objects.get(id=int(course_id))
	except:
		return HttpResponse("Disciplina não existente.")
	if course is not None:
		if request.user.is_authenticated():
			student = Student.objects.get(user=request.user)
			if student is not None:
				if course in student.courses.all():
					subscribe = False
				else:
					subscribe = True
				values['subscribe'] = subscribe
				values['course'] = course
				if request.method == 'POST':
					student.courses.add(course)
					student.save()
					return HttpResponseRedirect('/')
				else:
					return render_to_response('course.html', values)
			else:
				return HttpResponse("Usuário não é um estudante.")
		else:
			return HttpResponseRedirect('/login/')
	return HttpResponse("Disciplina não existente.")

def course_list(request):
	course_list = list(Course.objects.all())
	return render_to_response('course_list.html', {'course_list':  course_list})
	
def get_code(request):
    values = {}
    values.update(csrf(request))
    if request.method == 'GET':
        form = GetCodeForm()
    else:
        form = GetCodeForm(request.POST)
        if form.is_valid():
                                    
            code_file = open("/tmp/Code.java", 'w')
            code_file.write(request.POST['code'])
            code_file.close()
                
            test_file = open("/tmp/TestCode.java", 'w')
            test_file.write(request.POST['test'])
            test_file.close()
            
            junit_location = os.path.join(os.path.dirname(__file__), 'junit/junit.jar').replace('\\', '/')
    
            code_compile_command = "javac -classpath /tmp/:" + junit_location + " /tmp/Code.java"
            test_compile_command = "javac -classpath /tmp/:" + junit_location + " /tmp/TestCode.java"
            test_command = "java -classpath /tmp/:" + junit_location + " -Djava.security.manager org.junit.runner.JUnitCore TestCode"
            
            code_compile_args = shlex.split(code_compile_command)
            test_compile_args = shlex.split(test_compile_command)
            test_args = shlex.split(test_command)
            
            code_compile = Popen(code_compile_args, stdout=PIPE, stderr=PIPE)
            code_compile_output = code_compile.stderr.read()
            
            test_compile = Popen(test_compile_args, stdout=PIPE, stderr=PIPE)
            test_compile_output = test_compile.stderr.read()
            
            test = Popen(test_args, stdout=PIPE, stderr=PIPE)
            test_output = test.stdout.read()
            
            values["code_compile_output"] = code_compile_output
            values["test_compile_output"] = test_compile_output
            values["test_output"] = test_output
            
    values['form'] = form
    return render_to_response('get_code.html', values)
        


        
        
        
