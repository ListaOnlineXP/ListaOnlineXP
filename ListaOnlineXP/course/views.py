# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from authentication.decorators import *
from exerciselist.models import ExerciseList
from models import Course, CourseMember


@profile_required
def course(request, course_id):
    profile = request.user.get_profile()
    course_id = int(course_id)
    values = {}
    course = Course.objects.get(id=course_id)
    values['course'] = course
    values['user'] = request.user
    values['exercise_list'] = ExerciseList.objects.filter(course=course).all()
    values['subscribe'] = not CourseMember.is_member_of_course(profile,
                                                                course)
    return render_to_response('course.html', values)

@profile_required
def course_enroll(request, course_id):
    profile = request.user.get_profile()
    course_id = int(course_id)
    course = Course.objects.get(id=course_id)
    membership = CourseMember(course=course, profile=profile, role='S')
    membership.save()
    return HttpResponseRedirect(course.link())

@profile_required
def course_list(request):
    values = {}
    values['user'] = request.user
    values['course_list'] = list(Course.objects.all())
    return render_to_response('course_list.html', values)
