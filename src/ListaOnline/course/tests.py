#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from ListaOnline.course.models import Course
from ListaOnline.course.models import Teacher

class TeacherTestCase(TestCase):
    
    def setUp(self):
        self.teacher1 = Teacher.objects.create(name="Alfredo")
        self.teacher2 = Teacher.objects.create(name="Gerosa")
        self.teacher3 = Teacher.objects.create(name="Flávio")
        
    def testTeacherDB(self):
        self.assertEqual(Teacher.objects.get(name="Alfredo").name, "Alfredo")
        self.assertEqual(Teacher.objects.get(name="Gerosa").id, 2)
        self.assertNotEqual(Teacher.objects.get(id="3").name,"Alfredo")
        self.assertNotEqual(Teacher.objects.get(id="3").name,"Gerosa")
        self.assertEqual(Teacher.objects.count(), 3)

class CourseTestCase(TestCase):
    
    def setUp(self):
        self.teacher1 = Teacher.objects.create(name="Alfredo")
        self.teacher2 = Teacher.objects.create(name="Gerosa")
        self.course1 = Course.objects.create(code="MAC0110", name="Introdução à Computação", teacher=Teacher.objects.get(id=1))
        self.course2 = Course.objects.create(code="MAC0122", name="Algoritmos", teacher=Teacher.objects.get(id=2))

    def testExist(self):
        self.assertEqual(Course.objects.get(id=1).code, "MAC0110")
        self.assertEqual(Course.objects.get(teacher="Alfredo").code, "MAC0110")
        self.assertEqual(Course.objects.get(teacher="Alfredo").id, 1)
        self.assertEqual(Course.objects.get(id=1).name, "Introdução à Computação")
        self.assertEqual(Course.objects.get(teacher="Alfredo").name, "Introdução à Computação")
        self.assertNotEqual(Course.objects.get(id=1).teacher, Teacher.objects.get(name="Gerosa"))
        self.assertEqual(Course.objects.get(id=1).teacher, Teacher.objects.get(name="Alfredo"))
        self.assertEqual(Course.objects.get(id=2).code, "MAC0122")
        self.assertEqual(Course.objects.get(teacher="Gerosa").code, "MAC0122")
        self.assertEqual(Course.objects.get(id=2).name, "Algoritmos")
        self.assertEqual(Course.objects.get(teacher="Gerosa").name, "Algoritmos")
        self.assertNotEqual(Course.objects.get(id=2).teacher, Teacher.objects.get(name="Alfredo"))
        self.assertEqual(Course.objects.get(id=2).teacher, Teacher.objects.get(name="Gerosa"))
        
        
        
        
        
        
        
        
        
        
        
        
        