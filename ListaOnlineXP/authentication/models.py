# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    nusp = models.CharField(max_length=100)
    kind = models.CharField(max_length=1)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/admin/authentication/student/%i/" % self.id

    def is_enrolled(self, course):
        if (course in self.courses.all()):
            return True
        else:
            return False

class Student(Profile):
    courses = models.ManyToManyField('course.Course', blank=True)

class Teacher(Profile):
    courses = models.ForeignKey('course.Course', blank=True)
