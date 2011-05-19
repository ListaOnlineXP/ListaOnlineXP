# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.generic.list_detail import object_list

from models import Course
from authentication.models import Profile, Teacher, Student
from authentication.decorators import profile_required 
#from exerciselist.models import ExerciseList

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
    user = Profile.objects.get(user=request.user)
    value = {'user': user}
    if user.is_student():
        student = Student.objects.get(id=user.id)
        course_list = Course.objects.all()
    else:
        teacher = Teacher.objects.get(id=user.id)
        course_list = Course.objects.filter(teacher=teacher)
    return object_list(request, queryset=course_list, template_object_name='course', 
            template_name='course_list.html', extra_context=value)
