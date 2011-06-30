#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
import datetime
from models import *
from course.models import *
from authentication.models import *

class ExerciseListTestCase(TestCase):

    def setUp(self):

        #Setup for User tests
        self.user1 = User.objects.create(username=u"alfredo", password=u"alf")
        self.user2 = User.objects.create(username=u"gerosa", password=u"weasd")
        self.user3 = User.objects.create(username=u"flavio", password=u"1234")
        self.user4 = User.objects.create(username=u"koiti", password=u"lalala")
        self.user5 = User.objects.create(username=u"tsp", password=u"weasd")
        self.user6 = User.objects.create(username=u"milan", password=u"1234")

        #Setup for Teacher tests
        self.teacher1 = Teacher.objects.create(name=u"Alfredo", nusp=u"6431089", user=User.objects.get(id=2))
        self.teacher2 = Teacher.objects.create(name=u"Gerosa", nusp=u"6797000", user=User.objects.get(id=3))
        self.teacher3 = Teacher.objects.create(name=u"Flávio", nusp=u"123456", user=User.objects.get(id=4))

        #Setup for Student tests
        self.student1 = Student.objects.create(name=u"Steven Koiti Tsukamoto", nusp=u"6431089", user=User.objects.get(id=5))
        self.student2 = Student.objects.create(name=u"Thiago da Silva Pinheiro", nusp=u"6797000", user=User.objects.get(id=6))
        self.student3 = Student.objects.create(name=u"Bruno Milan Perfetto", nusp=u"123456", user=User.objects.get(id=7))

        #Setup for Course tests
        self.course1 = Course.objects.create(code=u"MAC0110", name=u"Introdução à Computação", teacher=Teacher.objects.get(id=1))
        self.course1.student.add(self.student1)
        self.course2 = Course.objects.create(code=u"MAC0342", name=u"XP", teacher=Teacher.objects.get(id=1))
        self.course3 = Course.objects.create(code=u"MAC0122", name=u"Algoritmos", teacher=Teacher.objects.get(id=2))


        #Setup for MultipleChoiceQuestion tests
        self.multichoicequestion1 = MultipleChoiceQuestion.objects.create(text=u"1+1?")
        self.multichoicequestion2 = MultipleChoiceQuestion.objects.create(text=u"O que é Refatoração?")
        self.multichoicequestion3 = MultipleChoiceQuestion.objects.create(text=u"")

        #Setup for MultipleChoiceCorrectAlternative tests
        self.multichoicecorrectalternative1 = MultipleChoiceCorrectAlternative.objects.create(text=u"2", question=MultipleChoiceQuestion.objects.get(id=1))
        self.multichoicecorrectalternative2 = MultipleChoiceCorrectAlternative.objects.create(text=u"blabl", question=MultipleChoiceQuestion.objects.get(id=2))
        self.multichoicecorrectalternative3 = MultipleChoiceCorrectAlternative.objects.create(text=u"", question=MultipleChoiceQuestion.objects.get(id=3))
        
        #Setup for ExerciseList tests
        self.exercise_list1 = ExerciseList.objects.create(name=u"Lista de exercícios 1", course=Course.objects.get(id=1))
#        self.exercise_list1.questions.add(self.multichoicequestion1)
#        self.exercise_list1.questions.add(self.multichoicequestion2)
        self.exercise_list2 = ExerciseList.objects.create(name=u"Lista de exercícios 2", course=self.course2, min_number_of_students = 1,max_number_of_students = 3)
#        self.exercise_list2.questions.add(self.multichoicequestion1)
#        self.exercise_list2.pub_date = (datetime.datetime.today() + datetime.timedelta(days=2))
#        self.exercise_list2.due_date = datetime.datetime.today()+datetime.timedelta(days=30)
        self.exercise_list3 = ExerciseList.objects.create(name=u"", course=self.course3, min_number_of_students = 1,max_number_of_students = 5)
#        self.exercise_list3.questions.add(self.multichoicequestion1)
#        self.exercise_list3.questions.add(self.multichoicequestion3)

        #Setup for JavaQuestion tests
        self.javaquestion = JavaQuestion.objects.create(text=u"Crie o helloworld.", criteria=u"Hello World!")
        self.javaquestion = JavaQuestion.objects.create(text=u"Crie um programa que some dois números.", criteria=u"1+2=3")

    def testMultipleChoiceQuestionDB(self):
        self.assertEqual(MultipleChoiceQuestion.objects.get(id=2).text, u"O que é Refatoração?")
        self.assertEqual(MultipleChoiceQuestion.objects.get(id=3).text, u"")
        self.assertNotEqual(MultipleChoiceQuestion.objects.get(text=u"1+1?").id, 2)
        self.assertNotEqual(MultipleChoiceQuestion.objects.get(id=1).text, u"")
        self.assertEqual(MultipleChoiceQuestion.objects.count(), 3)

    def testMultipleChoiceCorrectAlternativeDB(self):
        self.assertEqual(MultipleChoiceCorrectAlternative.objects.get(id=1).question, MultipleChoiceQuestion.objects.get(text=u"1+1?"))
        self.assertEqual(MultipleChoiceCorrectAlternative.objects.get(id=2).question, MultipleChoiceQuestion.objects.get(text=u"O que é Refatoração?"))
        self.assertEqual(MultipleChoiceCorrectAlternative.objects.get(id=3).question, MultipleChoiceQuestion.objects.get(text=u""))
        self.assertEqual(MultipleChoiceCorrectAlternative.objects.get(question=MultipleChoiceQuestion.objects.get(text=u"1+1?")).id, 1)
        self.assertEqual(MultipleChoiceCorrectAlternative.objects.get(question=MultipleChoiceQuestion.objects.get(text=u"")).id, 3)
        self.assertEqual(MultipleChoiceCorrectAlternative.objects.filter(question=MultipleChoiceQuestion.objects.get(text=u"1+1?"))[0].id, 1)
        self.assertEqual(MultipleChoiceCorrectAlternative.objects.filter(question=MultipleChoiceQuestion.objects.get(text=u"O que é Refatoração?"))[0].id, 2)
        self.assertNotEqual(MultipleChoiceCorrectAlternative.objects.get(id=1).question, MultipleChoiceQuestion.objects.get(text=u""))
        self.assertEqual(MultipleChoiceCorrectAlternative.objects.filter(question=MultipleChoiceQuestion.objects.get(text=u"1+1?")).count(), 1)
        self.assertEqual(MultipleChoiceCorrectAlternative.objects.count(), 3)
 
    def testExerciseListDB(self):
        self.assertEqual(ExerciseList.objects.get(name="Lista de exercícios 1").name, u"Lista de exercícios 1")
#       self.assertEqual(ExerciseList.objects.get(name="Lista de exercícios 1").questions.filter(text__contains=u"Refatoração")[0].text, self.multichoicequestion2.text)
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

    def testTeacherDB(self):
        self.assertEqual(Teacher.objects.get(name=u"Alfredo").name, u"Alfredo")
        self.assertEqual(Teacher.objects.get(name=u"Gerosa").id, 2)
        self.assertNotEqual(Teacher.objects.get(id=u"3").name,u"Alfredo")
        self.assertNotEqual(Teacher.objects.get(id=u"3").name,u"Gerosa")
        self.assertEqual(Teacher.objects.count(), 3)
