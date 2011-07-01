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
    values['user'] = user = Profile.objects.get(user=request.user)
    exercise_list = ExerciseList.objects.filter(course=course).all()
    if user.is_student():
        student = Student.objects.get(id=user.id)
        if student in course.student.all():
            values['subscribe'] = False
        else:
            values['subscribe'] = True
        if request.method == 'POST':
            course.student.add(student)
            course.save()
            return HttpResponseRedirect('/course/' + course_id)
    elif user.is_teacher():
        teacher = Teacher.objects.get(id=user.id)
        values['teacher'] = teacher
    return object_list(request, queryset=exercise_list, template_object_name='exercise', 
            template_name='course.html', extra_context=values)

@profile_required
def course_list(request):
    values = {}
    user = Profile.objects.get(user=request.user)
    values['user'] = user
    if user.is_teacher():
	values['teacher'] = Teacher.objects.get(id=user.id)
    course_list = Course.objects.all()
    return object_list(request, queryset=course_list, template_object_name='course', 
            template_name='course_list.html', extra_context=values)

@teacher_required
def course_add_or_update(request, course_id=None):
    if course_id:
        return update_object(request, model=Course, object_id=course_id, 
                template_name='course_form.html', post_save_redirect='/')
    else:
        return create_object(request, model=Course, 
                template_name='course_form.html', post_save_redirect='/')

@teacher_required
def course_delete(request, course_id):
    return delete_object(request, model=Course, object_id=course_id, 
            template_name='course_confirm_delete.html', post_delete_redirect='/')

@profile_required
def my_course_list(request):
    values = {}
    values['user'] = user = Profile.objects.get(user=request.user)
    if user.is_student():
        student = Student.objects.get(id=user.id)
        course_list = Course.objects.filter(student=student)
    elif user.is_teacher():
        teacher = Teacher.objects.get(id=user.id)
        values['teacher'] = teacher
        course_list = Course.objects.filter(teacher=teacher)
    return object_list(request, queryset=course_list, template_object_name='course', 
            template_name='course_list.html', extra_context=values)

#===BEGIN Course report===
@teacher_required
def report(request, course_id):
    values = {}
    values['user'] = Profile.objects.get(user=request.user)
    course = Course.objects.get(id=course_id)
    students = course.student.all()
    values['exercise_lists'] = exercise_lists = ExerciseList.objects.filter(course=course)
    values['students_report'] = [(student, student_report(student, exercise_lists)) for student in students]
    values['mean_lists'] = [exercise_list.mean() for exercise_list in exercise_lists]
    return render_to_response('report.html', values)

def student_report(student, exercise_lists):
    return [(student.get_group(exercise_list).solution, student.get_group(exercise_list).solution.get_not_corrected_answers().count) for exercise_list in exercise_lists]
#===END Course report===
