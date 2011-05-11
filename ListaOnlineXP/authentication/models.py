# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):

    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=100)
    nusp = models.CharField(max_length=100)
    favourite_color = models.CharField(max_length=10)
    courses = models.ManyToManyField('course.Course', blank=True)
   
    def get_absolute_url(self):
            return "/admin/authentication/student/%i/" % self.id

    def __unicode__(self):
        return self.name 

    def is_enrolled(self, course):
        if (course in self.courses.all()):
            return True
        else:
            return False
