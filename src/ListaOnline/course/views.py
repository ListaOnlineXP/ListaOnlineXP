# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from forms import NewStudentForm, StudentLoginForm, CheckJavaForm
from models import Student, Teacher, Course

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
	
	
	
def check_java(request):
    values = {}
    values.update(csrf(request))
    if request.method == 'GET':
        form = CheckJavaForm()
    else:
        form = CheckJavaForm(request.POST)
        if form.is_valid():
            
            
            
            return HttpResponseRedirect('/check_java/result')
    values['form'] = form
    return render_to_response('check_java.html', values)
        

    pass
