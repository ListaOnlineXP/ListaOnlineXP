# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from authentication.decorators import profile_required 
from models import Course
#from exerciselist.models import ExerciseList
from authentication.models import Teacher, Student

@profile_required
def course(request, course_id):
    values = {}
    values.update(csrf(request))
    try:
        course = Course.objects.get(id=int(course_id))
    except:
        raise Http404
    if course is not None:
        student = Student.objects.get(user=request.user)
        values['course'] = course
        values['student'] = student
        if course in student.courses.all():
            exercise_list = ExerciseList.objects.filter(course=course)
            values['exercise_list'] = list(exercise_list)
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
    raise Http404

@profile_required
def course_list(request):
    values = {}
    values['student'] = Student.objects.get(user=request.user)
    values['course_list'] = list(Course.objects.all())
    return render_to_response('course_list.html', values)


