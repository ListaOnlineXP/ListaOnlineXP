#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
import datetime
from models import *
from course.models import *

class ExerciseListTestCase(TestCase):

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

        #Setup for MultipleChoiceQuestion tests
        self.multichoicequestion1 = MultipleChoiceQuestion.objects.create(text=u"1+1?")
        self.multichoicequestion2 = MultipleChoiceQuestion.objects.create(text=u"O que é Refatoração?")
        self.multichoicequestion3 = MultipleChoiceQuestion.objects.create(text=u"")

        #Setup for MultipleChoiceCorrectAnswer tests
        self.multichoicecorrectanswer1 = MultipleChoiceCorrectAnswer.objects.create(question=MultipleChoiceQuestion.objects.get(id=1))
        self.multichoicecorrectanswer2 = MultipleChoiceCorrectAnswer.objects.create(question=MultipleChoiceQuestion.objects.get(id=2))
        self.multichoicecorrectanswer3 = MultipleChoiceCorrectAnswer.objects.create(question=MultipleChoiceQuestion.objects.get(id=3))
        
        #Setup for ExerciseList tests
        self.exercise_list1 = ExerciseList.objects.create(name=u"Lista de exercícios 1", course=self.course1)
        self.exercise_list1.questions.add(self.multichoicequestion1)
        self.exercise_list1.questions.add(self.multichoicequestion2)
        self.exercise_list2 = ExerciseList.objects.create(name=u"Lista de exercícios 2", course=self.course2)
        self.exercise_list2.questions.add(self.multichoicequestion1)
        self.exercise_list2.pub_date = datetime.datetime.today()+datetime.timedelta(days=2)
        self.exercise_list2.due_date = datetime.datetime.today()+datetime.timedelta(days=30)
        self.exercise_list3 = ExerciseList.objects.create(name=u"", course=self.course3)
        self.exercise_list3.questions.add(self.multichoicequestion1)
        self.exercise_list3.questions.add(self.multichoicequestion3)
        #Setup for JavaQuestion tests
        self.javaquestion = JavaQuestion.objects.create(text=u"Crie o helloworld.", criteria=u"Hello World!")
        self.javaquestion = JavaQuestion.objects.create(text=u"Crie um programa que some dois números.", criteria=u"1+2=3")

    def testMultipleChoiceQuestionDB(self):
        self.assertEqual(MultipleChoiceQuestion.objects.get(id=2).text, u"O que é Refatoração?")
        self.assertEqual(MultipleChoiceQuestion.objects.get(id=3).text, u"")
        self.assertNotEqual(MultipleChoiceQuestion.objects.get(text=u"1+1?").id, 2)
        self.assertNotEqual(MultipleChoiceQuestion.objects.get(id=1).text, u"")
        self.assertEqual(MultipleChoiceQuestion.objects.count(), 3)

    def testMultipleChoiceCorrectAnswerDB(self):
        self.assertEqual(MultipleChoiceCorrectAnswer.objects.get(id=1).question, MultipleChoiceQuestion.objects.get(text=u"1+1?"))
        self.assertEqual(MultipleChoiceCorrectAnswer.objects.get(id=2).question, MultipleChoiceQuestion.objects.get(text=u"O que é Refatoração?"))
        self.assertEqual(MultipleChoiceCorrectAnswer.objects.get(id=3).question, MultipleChoiceQuestion.objects.get(text=u""))
        self.assertEqual(MultipleChoiceCorrectAnswer.objects.get(question=MultipleChoiceQuestion.objects.get(text=u"1+1?")).id, 1)
        self.assertEqual(MultipleChoiceCorrectAnswer.objects.get(question=MultipleChoiceQuestion.objects.get(text=u"")).id, 3)
        self.assertEqual(MultipleChoiceCorrectAnswer.objects.filter(question=MultipleChoiceQuestion.objects.get(text=u"1+1?"))[0].id, 1)
        self.assertEqual(MultipleChoiceCorrectAnswer.objects.filter(question=MultipleChoiceQuestion.objects.get(text=u"O que é Refatoração?"))[0].id, 2)
        self.assertNotEqual(MultipleChoiceCorrectAnswer.objects.get(id=1).question, MultipleChoiceQuestion.objects.get(text=u""))
        self.assertEqual(MultipleChoiceCorrectAnswer.objects.filter(question=MultipleChoiceQuestion.objects.get(text=u"1+1?")).count(), 1)
        self.assertEqual(MultipleChoiceCorrectAnswer.objects.count(), 3)

    def testExerciseListDB(self):
        self.assertEqual(ExerciseList.objects.get(name="Lista de exercícios 1").name, u"Lista de exercícios 1")
        self.assertEqual(ExerciseList.objects.get(name="Lista de exercícios 1").questions.filter(text__contains=u"Refatoração")[0].text, self.multichoicequestion2.text)
        self.assertEqual(ExerciseList.objects.count(), 3)
        self.exercise_list3.delete()
        self.assertEqual(ExerciseList.objects.count(), 2)
        for exercise_list in ExerciseList.objects.all():
            exercise_list.delete()
        self.assertEqual(ExerciseList.objects.count(), 0)


    def testJavaQuestion(self):
        self.assertEqual(JavaQuestion.objects.get(text=u"Crie o helloworld.").criteria, u"Hello World!")
        self.assertEqual(JavaQuestion.objects.get(criteria=u"1+2=3").text, u"Crie um programa que some dois números.")
        self.assertEqual(JavaQuestion.objects.count(), 2)
