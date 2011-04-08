# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from forms import NewStudentForm, StudentLoginForm, GetCodeForm
from models import Student, Teacher, Course

import os.path
from subprocess import Popen, PIPE
import shlex

def student(request):
	student = Student.objects.get(user=request.user)
	if student is not None:
		return render_to_response('student.html', {'student': student})
	else:
		return HttpResponse('Estudante invalido.')

def new_student(request):
	values = {}
	values.update(csrf(request))
	if request.method == 'GET':
		form = NewStudentForm()
	else:
		form = NewStudentForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			username = form.cleaned_data['username']
			passwd = form.cleaned_data['passwd']
			try:
				user = User.objects.create_user(username, 'teste@teste.com', passwd)
				student = Student(name=name, user=user)
				student.save()
				user = authenticate(username=username, password=passwd)
				login(request, user)
				return HttpResponseRedirect('/student/')
			except:
				form._errors["username"] = form.error_class(["Usuario ja cadastrado."])
	values['form'] = form
	return render_to_response('new_student.html', values)

def student_login(request):
	values = {}
	values.update(csrf(request))
	if request.method == 'GET':
		form = StudentLoginForm()
	else:
		form = StudentLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			passwd = form.cleaned_data['passwd']
			try:
				user = User.objects.get(username=username)
				if user.check_password(passwd):
					user = authenticate(username=username, password=passwd)
					login(request, user)
					return HttpResponseRedirect('/student/')
				else:
					form._errors['passwd'] = form.error_class(['Senha incorreta.'])
			except:
				form._errors['username'] = form.error_class(['Usuario nao cadastrado.'])
	values['form'] = form
	return render_to_response('student_login.html', values)

def student_logout(request):
	logout(request)
	return HttpResponseRedirect('/student/login/')

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
        


        
        
        