# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from models import Profile, Student, Teacher
from exerciselist.models import *

def check_lists_date():
    late_solutions = ExerciseListSolution.objects.filter(exercise_list__due_date__lt=datetime.datetime.today())

    for late_solution in late_solutions:
        late_solution.finalized=True

def profile_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    def test_profile(user):
        return user.is_authenticated() and not user.is_staff

    check_lists_date()

    actual_decorator = user_passes_test(
        test_profile,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
   

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    def test_student(user):
        try:
            student = Student.objects.get(user=user)
        except:
            return False
        return user.is_authenticated() and not user.is_staff

    check_lists_date()

    actual_decorator = user_passes_test(
        test_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
   

def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    def test_teacher(user):
        try:
            teacher = Teacher.objects.get(user=user)
        except:
            return False
        return user.is_authenticated() and not user.is_staff

    check_lists_date()

    actual_decorator = user_passes_test(
        test_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
