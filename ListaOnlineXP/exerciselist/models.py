# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
import datetime

class Question(models.Model):

    text = models.TextField()

    def __unicode__(self):
        return self.text
        

class MultipleChoiceQuestion(Question):

    def get_correct_alternative(self):
        #Returns the multiple choice question's correct answer object
        return MultipleChoiceCorrectAlternative.objects.get(question=self)

    def get_alternatives(self):
        #Returns a QuerySet with all of the multiplechoice question's alternatives
        return MultipleChoiceAlternative.objects.filter(Q(multiplechoicecorrectalternative__question=self) | Q(multiplechoicewrongalternative__question=self))
    


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
    
    def __unicode__(self):
        return self.name


class ExerciseListSolution(models.Model):
    
    student = models.ForeignKey('authentication.Student')
    exercise_list = models.ForeignKey(ExerciseList)
    
class Answer(models.Model):
    
    exercise_list_solution = models.ForeignKey(ExerciseListSolution)

class MultipleChoiceQuestionAnswer(Answer):
    
    question_answered = models.ForeignKey(MultipleChoiceQuestion)
    
class JavaQuestionAnswer(Answer):
    
    code = models.TextField(blank=False)

