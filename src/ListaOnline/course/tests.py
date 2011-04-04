#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
from models import Course, Teacher, Question, ExerciseList

class CourseTestCase(TestCase):
    
    def setUp(self):
        self.teacher1 = Teacher.objects.create(name=u"Alfredo")
        self.teacher2 = Teacher.objects.create(name=u"Gerosa")
        self.teacher3 = Teacher.objects.create(name=u"Flávio")
        self.course1 = Course.objects.create(code=u"MAC0110", name=u"Introdução à Computação", teacher=Teacher.objects.get(id=1))
        self.course2 = Course.objects.create(code=u"MAC0342", name=u"XP", teacher=Teacher.objects.get(id=1))
        self.course3 = Course.objects.create(code=u"MAC0122", name=u"Algoritmos", teacher=Teacher.objects.get(id=2))
        self.question1 = Question.objects.create(text=u"1+1?")
        self.question2 = Question.objects.create(text=u"O que é Refatoração?")
        self.question3 = Question.objects.create(text=u"")

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

    def testQuestionDB(self):
        self.assertEqual (Question.objects.get(id=2).text, u"O que é Refatoração?")
        self.assertEqual (Question.objects.get(id=3).text, u"")
        self.assertNotEqual (Question.objects.get(text=u"1+1?").id, 2)
        self.assertNotEqual (Question.objects.get(id=3).text, "O que é Refatoração?")

    def testExerciseListaDB(self):
        pass
