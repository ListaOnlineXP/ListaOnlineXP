# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from models import Teacher, Course
from authentication.models import Student
from authentication.views import get_student, get_admin


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


