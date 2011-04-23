#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
from models import  Student
from django.contrib.auth.models import User

class CourseTestCase(TestCase):
    
    def setUp(self):
        
        #Setup for Student tests
        self.user1 = User.objects.create(username=u"koiti", password=u"lalala")
        self.user2 = User.objects.create(username=u"tsp", password=u"weasd")
        self.user3 = User.objects.create(username=u"milan", password=u"1234")
        self.student1 = Student.objects.create(name=u"Steven Koiti Tsukamoto", nusp=u"6431089", user=User.objects.get(id=1))
        self.student2 = Student.objects.create(name=u"Thiago da Silva Pinheiro", nusp=u"6797000", user=User.objects.get(id=2))
        self.student3 = Student.objects.create(name=u"Bruno Milan Perfetto", nusp=u"123456", user=User.objects.get(id=3))
        
    def testStudentDB(self):

        self.assertEqual(Student.objects.get(name=u"Steven Koiti Tsukamoto").name, u"Steven Koiti Tsukamoto")
        self.assertEqual(Student.objects.get(name=u"Thiago da Silva Pinheiro").id, 2)
        self.assertEqual(Student.objects.get(name=u"Bruno Milan Perfetto").nusp, u"123456")
        self.assertEqual(Student.objects.get(name=u"Thiago da Silva Pinheiro").user.username, u"tsp")
        self.assertNotEqual(Student.objects.get(id=u"3").name,u"Steven Koiti Tsukamoto")
        self.assertNotEqual(Student.objects.get(id=u"3").name,u"Thiago da Silva Pinheiro")
        self.assertEqual(Student.objects.count(), 3)

