# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object, update_object, delete_object

from models import Course
from authentication.models import Profile, Teacher, Student
from authentication.decorators import profile_required, teacher_required
from exerciselist.models import ExerciseList

@profile_required
def course(request, course_id):
    values = {}
    values.update(csrf(request))
    values['course'] = course = get_object_or_404(Course, id=int(course_id))
    if course is not None:
        values['user'] = user = Profile.objects.get(user=request.user)
        if user.is_student():
            student = Student.objects.get(id=user.id)
            if student in course.student.all():
                values['exercise_list'] = exercise_list = ExerciseList.objects.filter(course=course).all()
                subscribe = False
            else:
                subscribe = True
            values['subscribe'] = subscribe
            if request.method == 'POST':
                course.student.add(student)
                course.save()
                return HttpResponseRedirect('/')
            else:
                return render_to_response('course.html', values)

@profile_required
def course_list(request):
    values = {}
    user = Profile.objects.get(user=request.user)
    values['user'] = user
    if user.is_student():
        student = Student.objects.get(id=user.id)
        course_list = Course.objects.all()
    elif user.is_teacher():
        teacher = Teacher.objects.get(id=user.id)
        values['teacher'] = teacher
        course_list = Course.objects.filter(teacher=teacher)
    return object_list(request, queryset=course_list, template_object_name='course', 
            template_name='course_list.html', extra_context=values)

@teacher_required
def course_add_or_update(request, key=None):
    if key:
        return update_object(request, model=Course, object_id=key, template_name='course_form.html')
    else:
        return create_object(request, model=Course, template_name='course_form.html', post_save_redirect='course')
