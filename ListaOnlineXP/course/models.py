# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True)
    teacher = models.ForeignKey(Teacher)
    
    def __unicode__(self):
        return self.name 

class Student(models.Model):

    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=100)
    nusp = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)
    
    def __unicode__(self):
        return self.name 


    

    
    
    
    
    
    
    
    
