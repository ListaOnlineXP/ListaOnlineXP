#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
from models import Course, Teacher, Student
from django.contrib.auth.models import User

class CourseTestCase(TestCase):
    
    def setUp(self):
        
        #Setup for Teacher tests
        self.teacher1 = Teacher.objects.create(name=u"Alfredo")
        self.teacher2 = Teacher.objects.create(name=u"Gerosa")
        self.teacher3 = Teacher.objects.create(name=u"Flávio")

        #Setup for Course tests
        self.course1 = Course.objects.create(code=u"MAC0110", name=u"Introdução à Computação", teacher=Teacher.objects.get(id=1))
        self.course2 = Course.objects.create(code=u"MAC0342", name=u"XP", teacher=Teacher.objects.get(id=1))
        self.course3 = Course.objects.create(code=u"MAC0122", name=u"Algoritmos", teacher=Teacher.objects.get(id=2))

               
        #Setup for Student tests
        self.user1 = User.objects.create(username=u"koiti", password=u"lalala")
        self.user2 = User.objects.create(username=u"tsp", password=u"weasd")
        self.user3 = User.objects.create(username=u"milan", password=u"1234")
        self.student1 = Student.objects.create(name=u"Steven Koiti Tsukamoto", nusp=u"6431089", user=User.objects.get(id=1))
        self.student2 = Student.objects.create(name=u"Thiago da Silva Pinheiro", nusp=u"6797000", user=User.objects.get(id=2))
        self.student3 = Student.objects.create(name=u"Bruno Milan Perfetto", nusp=u"123456", user=User.objects.get(id=3))
        
    def testTeacherDB(self):
        self.assertEqual(Teacher.objects.get(name=u"Alfredo").name, u"Alfredo")
        self.assertEqual(Teacher.objects.get(name=u"Gerosa").id, 2)
        self.assertNotEqual(Teacher.objects.get(id=u"3").name,u"Alfredo")
        self.assertNotEqual(Teacher.objects.get(id=u"3").name,u"Gerosa")
        self.assertEqual(Teacher.objects.count(), 3)

    def testCourseDB(self):
        self.assertEqual(Course.objects.get(id=1).code, u"MAC0110")
        self.assertEqual(Course.objects.get(id=2).code, u"MAC0342")
        self.assertEqual(Course.objects.get(id=3).code, u"MAC0122")
        self.assertEqual(Course.objects.get(id=1).teacher, Teacher.objects.get(name=u"Alfredo"))
        self.assertEqual(Course.objects.get(id=2).teacher, Teacher.objects.get(name=u"Alfredo"))
        self.assertEqual(Course.objects.get(id=3).teacher, Teacher.objects.get(name=u"Gerosa"))
        self.assertEqual(Course.objects.get(id=1).name, u"Introdução à Computação")
        self.assertEqual(Course.objects.get(id=2).name, u"XP")
        self.assertEqual(Course.objects.get(id=3).name, u"Algoritmos")
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name=u"Alfredo"))[0].id, 1)
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name=u"Alfredo"))[1].id, 2)
        self.assertEqual(Course.objects.get(teacher=Teacher.objects.get(name=u"Gerosa")).id, 3)
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name=u"Alfredo"))[0].code, u"MAC0110")
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name=u"Alfredo"))[1].code, u"MAC0342")
        self.assertEqual(Course.objects.get(teacher=Teacher.objects.get(name=u"Gerosa")).code, u"MAC0122")
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name=u"Alfredo"))[0].name, u"Introdução à Computação")
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name=u"Alfredo"))[1].name, u"XP")
        self.assertEqual(Course.objects.get(teacher=Teacher.objects.get(name=u"Gerosa")).name, u"Algoritmos")
        self.assertNotEqual(Course.objects.get(id=1).teacher, Teacher.objects.get(name=u"Gerosa"))
        self.assertNotEqual(Course.objects.get(id=2).teacher, Teacher.objects.get(name=u"Flávio"))
        self.assertNotEqual(Course.objects.get(id=3).teacher, Teacher.objects.get(name=u"Alfredo"))
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name=u"Alfredo")).count(), 2)
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name=u"Gerosa")).count(), 1)
        self.assertEqual(Course.objects.filter(teacher=Teacher.objects.get(name=u"Flávio")).count(), 0)
        self.assertEqual([self.course1, self.course2], [self.course1, self.course2])
        self.assertEqual(list(Course.objects.filter(teacher=Teacher.objects.get(name=u"Alfredo"))), [self.course1, self.course2])
        self.assertEqual(Course.objects.count(), 3)

         
    def testStudentDB(self):
        self.assertEqual(Student.objects.get(name=u"Steven Koiti Tsukamoto").name, u"Steven Koiti Tsukamoto")
        self.assertEqual(Student.objects.get(name=u"Thiago da Silva Pinheiro").id, 2)
        self.assertEqual(Student.objects.get(name=u"Bruno Milan Perfetto").nusp, u"123456")
        self.assertEqual(Student.objects.get(name=u"Thiago da Silva Pinheiro").user.username, u"tsp")
        self.assertNotEqual(Student.objects.get(id=u"3").name,u"Steven Koiti Tsukamoto")
        self.assertNotEqual(Student.objects.get(id=u"3").name,u"Thiago da Silva Pinheiro")
        self.assertEqual(Student.objects.count(), 3)

