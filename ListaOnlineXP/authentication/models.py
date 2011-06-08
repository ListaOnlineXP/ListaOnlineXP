# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True)
    name = models.CharField(max_length=100)
    nusp = models.CharField(max_length=100)

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

    def __unicode__(self):
        return self.name

class Student(Profile):
    pass

class Teacher(Profile):
    pass

class Group(models.Model):
    students = models.ManyToManyField(Student)
    solution = models.OneToOneField('exerciselist.ExerciseListSolution', blank=True)
