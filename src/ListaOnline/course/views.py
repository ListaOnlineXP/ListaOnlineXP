from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from course.models import Teacher
from course.models import Course

def index(request, course_id):
    try:
	course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
	raise Http404
    student_list = [course.teacher]
    return render_to_response('course/students.html', {'student_list':  student_list, 'course': course})
