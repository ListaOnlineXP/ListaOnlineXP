# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    nusp = models.CharField(max_length=100)

    def is_enrolled(self, course):
        if (course in self.courses.all()):
            return True
        else:
            return False

    def is_student(self):
        try:
            Student.objects.get(id=self.id)
        except Profile.DoesNotExist:
            return False
        return True

    def is_teacher(self):
        try:
            Teacher.objects.get(id=self.id)
        except Profile.DoesNotExist:
            return False
        return True

    def get_absolute_url(self):
        return "/admin/authentication/student/%i/" % self.id

    def __unicode__(self):
        return self.name

class Student(Profile):
    pass

class Teacher(Profile):
    pass
