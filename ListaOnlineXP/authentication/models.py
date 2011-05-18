# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    nusp = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/admin/authentication/student/%i/" % self.id

    def is_enrolled(self, course):
        if (course in self.courses.all()):
            return True
        else:
            return False

    def is_student(self):
	try:
	    Student.objects.get(pk=self.pk)
	except Profile.DoesNotExist:
	    return False
	return True

    def is_teacher(self):
	try:
	    Teacher.objects.get(pk=self.pk)
	except Profile.DoesNotExist:
	    return False
	return True
	

class Student(Profile):
    courses = models.ManyToManyField('course.Course', blank=True)

class Teacher(Profile):
    courses = models.ForeignKey('course.Course', blank=True)

