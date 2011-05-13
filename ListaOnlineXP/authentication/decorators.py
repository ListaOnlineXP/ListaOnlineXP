# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from models import Profile

def profile_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    def test_profile(user):
        return user.is_authenticated() and not user.is_staff

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
            student = Profile.objects.get(user=user, kind='S')
        except:
            return False
        return user.is_authenticated() and not user.is_staff

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
            teacher = Profile.objects.get(user=user, kind='T')
        except:
            return False
        return user.is_authenticated() and not user.is_staff

    actual_decorator = user_passes_test(
        test_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
