#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
from models import Course, Teacher, MultipleChoiceQuestion, MultipleChoiceCorrectAnswer, ExerciseList
import datetime

class CourseTestCase(TestCase):
    
    def setUp(self):
        self.teacher1 = Teacher.objects.create(name=u"Alfredo")
        self.teacher2 = Teacher.objects.create(name=u"Gerosa")
        self.teacher3 = Teacher.objects.create(name=u"Flávio")
        self.course1 = Course.objects.create(code=u"MAC0110", name=u"Introdução à Computação", teacher=Teacher.objects.get(id=1))
        self.course2 = Course.objects.create(code=u"MAC0342", name=u"XP", teacher=Teacher.objects.get(id=1))
        self.course3 = Course.objects.create(code=u"MAC0122", name=u"Algoritmos", teacher=Teacher.objects.get(id=2))
        self.multichoicequestion1 = MultipleChoiceQuestion.objects.create(text=u"1+1?")
        self.multichoicequestion2 = MultipleChoiceQuestion.objects.create(text=u"O que é Refatoração?")
        self.multichoicequestion3 = MultipleChoiceQuestion.objects.create(text=u"")
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
