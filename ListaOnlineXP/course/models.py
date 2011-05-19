# -*- coding: utf-8 -*-
from django.db import models
from authentication.models import Student, Teacher

class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True)
    teacher = models.ForeignKey(Teacher)
    student = models.ManyToManyField(Student, blank=True)
    
    def __unicode__(self):
        return self.name 
