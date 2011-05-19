# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
import datetime

from itertools import izip
from random import shuffle

#Exercise List
class Question(models.Model):
    text = models.TextField()

    def __unicode__(self):
        return self.text


class DiscursiveQuestion(Question):
    pass


class MultipleChoiceQuestion(Question):
    def get_correct_alternative(self):
        #Returns the multiple choice question's correct answer object
        return MultipleChoiceCorrectAlternative.objects.get(question=self)

    def get_alternatives(self):
        #Returns a QuerySet with all of the multiplechoice question's alternatives
        return MultipleChoiceAlternative.objects.filter(Q(multiplechoicecorrectalternative__question=self) | 
                Q(multiplechoicewrongalternative__question=self))


class JavaQuestion(Question):
    criteria = models.TextField()


class MultipleChoiceAlternative(models.Model):
    text = models.CharField(blank=False, max_length=300)    

    def __unicode__(self):
        return self.text        


class MultipleChoiceCorrectAlternative(MultipleChoiceAlternative):
    question = models.OneToOneField(MultipleChoiceQuestion) 
    
    
class MultipleChoiceWrongAlternative(MultipleChoiceAlternative):
    question = models.ForeignKey(MultipleChoiceQuestion)
    

class ExerciseList(models.Model):
    name = models.CharField(blank=False, max_length=100)
    course = models.ForeignKey('course.Course')
    pub_date = models.DateField(default=datetime.datetime.today)
    due_date = models.DateField(default=(datetime.datetime.today()+datetime.timedelta(days=7)))
    questions = models.ManyToManyField(Question)

    def get_multiple_choice_questions(self):
        return MultipleChoiceQuestion.objects.filter(exerciselist=self)

    def get_java_questions(self):
        return JavaQuestion.objects.filter(exerciselist=self)

    def get_discursive_questions(self):
        return DiscursiveQuestion.objects.filter(exerciselist=self)

    def get_questions_alternatives(self):
        questions = self.questions.all()
        alternatives = []
        for question in questions:
            multiple_choice_question = MultipleChoiceQuestion.objects.get(pk=question.pk)
            alternatives.append(list(multiple_choice_question.get_alternatives()))
        return izip(questions, alternatives)

    def __unicode__(self):
        return self.name


class ExerciseListSolution(models.Model):
    student = models.ForeignKey('authentication.Student')
    exercise_list = models.ForeignKey(ExerciseList)


class Answer(models.Model):
    exercise_list_solution = models.ForeignKey(ExerciseListSolution, editable=False)
    question_answered = models.ForeignKey(Question, editable=False)


class DiscursiveQuestionAnswer(Answer):
    text = models.TextField(blank=False)


class MultipleChoiceQuestionAnswer(Answer):
    chosen_alternative = models.ForeignKey(MultipleChoiceAlternative)
    

class JavaQuestionAnswer(Answer):
    code = models.TextField(blank=False)
