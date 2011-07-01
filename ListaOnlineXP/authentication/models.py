# -*- coding: utf-8 -*-
from django.db import models
from models import *
from datetime import datetime
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
    #Get Group filtering Student
    def get_group(self, exercise_list):
        groups = Group.objects.filter(solution__exercise_list = exercise_list).all()
        group = None
        for gr in groups:
            if self in gr.students.all():
                group = gr
        return group


class Teacher(Profile):
    pass

class Group(models.Model):
    students = models.ManyToManyField(Student, blank=True)
    solution = models.OneToOneField('exerciselist.ExerciseListSolution')

    def __unicode__(self):
        s = ''
        for student in self.students.all():
            s += student.name + ', '
        s = s[:-2]
        return s
