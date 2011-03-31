#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
from ListaOnline.course.models import Course
from ListaOnline.course.models import Teacher

class CourseTestCase(TestCase):
    
    def setUp(self):
        self.teacher1 = Teacher.objects.create(name="Alfredo")
        self.teacher2 = Teacher.objects.create(name="Gerosa")
        self.teacher3 = Teacher.objects.create(name="Flávio")
        self.course1 = Course.objects.create(code="MAC0110", name="Introdução à Computação", teacher=Teacher.objects.get(id=1))
        self.course2 = Course.objects.create(code="MAC0342", name="XP", teacher=Teacher.objects.get(id=1))
        self.course3 = Course.objects.create(code="MAC0122", name="Algoritmos", teacher=Teacher.objects.get(id=2))

    def testTeacherDB(self):
        self.assertEqual(Teacher.objects.get(name="Alfredo").name, "Alfredo")
        self.assertEqual(Teacher.objects.get(name="Gerosa").id, 2)
        self.assertNotEqual(Teacher.objects.get(id="3").name,"Alfredo")
        self.assertNotEqual(Teacher.objects.get(id="3").name,"Gerosa")
        self.assertEqual(Teacher.objects.count(), 3)

    def testCourseDB(self):
        self.assertEqual(Course.objects.get(id=1).code, "MAC0110")
        self.assertEqual(Course.objects.get(id=2).code, "MAC0342")
        self.assertEqual(Course.objects.get(id=3).code, "MAC0122")
        self.assertEqual(Course.objects.get(id=1).teacher, Teacher.objects.get(name="Alfredo"))
        self.assertEqual(Course.objects.get(id=2).teacher, Teacher.objects.get(name="Alfredo"))
        self.assertEqual(Course.objects.get(id=3).teacher, Teacher.objects.get(name="Gerosa"))
#       self.assertEqual(Course.objects.get(id=1).name, "Introdução à Computação")
        self.assertEqual(Course.objects.get(id=2).name, "XP")
        self.assertEqual(Course.objects.get(id=3).name, "Algoritmos")
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name="Alfredo"))[0].id, 1)
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name="Alfredo"))[1].id, 2)
        self.assertEqual(Course.objects.get(teacher=Teacher.objects.get(name="Gerosa")).id, 3)
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name="Alfredo"))[0].code, "MAC0110")
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name="Alfredo"))[1].code, "MAC0342")
        self.assertEqual(Course.objects.get(teacher=Teacher.objects.get(name="Gerosa")).code, "MAC0122")
#       self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name="Alfredo"))[0].name, "Introdução à Computação")
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name="Alfredo"))[1].name, "XP")
        self.assertEqual(Course.objects.get(teacher=Teacher.objects.get(name="Gerosa")).name, "Algoritmos")
        self.assertNotEqual(Course.objects.get(id=1).teacher, Teacher.objects.get(name="Gerosa"))
        self.assertNotEqual(Course.objects.get(id=2).teacher, Teacher.objects.get(name="Flávio"))
        self.assertNotEqual(Course.objects.get(id=3).teacher, Teacher.objects.get(name="Alfredo"))
	self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name="Alfredo")).count(), 2)
	self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name="Gerosa")).count(), 1)
	self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name="Flávio")).count(), 0)
#       self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name="Alfredo")), (self.course1, self.course2))
	self.assertEqual(Course.objects.count(), 3)
