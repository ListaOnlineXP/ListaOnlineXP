# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from models import Profile


def profile_required(function=None,
                     redirect_field_name=REDIRECT_FIELD_NAME,
                     login_url=None):
    def test_student_or_teacher(user):
        try:
            profile = Profile.objects.get(user=user)
            return True
        except:
            pass
        return False

    actual_decorator = user_passes_test(
        test_student_or_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
   
   
def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
                     login_url=None):
    def test_teacher(user):
        try:
            profile = Profile.objects.get(user=user)
            return profile.is_teacher()
        except:
            pass
        return False

    actual_decorator = user_passes_test(
        test_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
