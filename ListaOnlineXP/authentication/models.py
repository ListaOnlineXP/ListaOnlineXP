# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    nusp = models.CharField(max_length=100)
    #courses = models.ManyToManyField('course.Course', blank=True)
    kind = models.CharField(max_length=1)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/admin/authentication/student/%i/" % self.id

    def is_enrolled(self, course):
        return True
        #if (course in self.courses.all()):
        #    return True
        #else:
        #    return False
