# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
import datetime

class Question(models.Model):

    text = models.TextField()

    def __unicode__(self):
        return self.text
        

class MultipleChoiceQuestion(Question):

    def get_correct_answer(self):
        #Returns the multiple choice question's correct answer object
        return MultipleChoiceCorrectAnswer.objects.get(question=self)

    def get_answers(self):
        #Returns a QuerySet with all of the multiplechoice question's answers
        return MultipleChoiceAnswer.objects.filter(Q(multiplechoicecorrectanswer__question=self) | Q(multiplechoicewronganswer__question=self))
        pass
    


class JavaQuestion(Question):

    criteria = models.TextField()


class MultipleChoiceAnswer(models.Model):

    text = models.CharField(blank=False, max_length=300)    

    def __unicode__(self):
        return self.text        


class MultipleChoiceCorrectAnswer(MultipleChoiceAnswer):

    question = models.OneToOneField(MultipleChoiceQuestion) 
    
    
class MultipleChoiceWrongAnswer(MultipleChoiceAnswer):

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

