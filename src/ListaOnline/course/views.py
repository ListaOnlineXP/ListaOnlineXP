from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from forms import NewStudentForm, StudentLoginForm
from models import Student

def new_student(request):
	values = {}
	values.update(csrf(request))
	if request.method == 'GET':
		form = NewStudentForm()
	else:
		form = NewStudentForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			nusp = form.cleaned_data['nusp']
			passwd = form.cleaned_data['passwd']
			student = Student(name=name, username=nusp, password=passwd)
			student.save()
			return HttpResponseRedirect('/')
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
			nusp = form.cleaned_data['nusp']
			passwd = form.cleaned_data['passwd']
			return HttpResponse('Ola, %s' % nusp)
	values['form'] = form
	return render_to_response('student_login.html', values)
