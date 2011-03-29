from django.db import models
import datetime

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True)
    teacher = models.ForeignKey(Teacher)
    
    def __unicode__(self):
        return self.name

class Question(models.Model):

    text = models.TextField(blank=False)

    def __unicode__(self):
        return self.text
        
class Answer(models.Model):

    text = models.TextField(blank=False)
    question = models.ForeignKey(Question, related_name="question")
    answer = models.OneToOneField(Question, related_name="answer")

    def __unicode__(self):
        return self.text        

class ExerciseList(models.Model):
    
    name = models.CharField(blank=False, max_length=100)
    course = models.ForeignKey(Course)
    pub_date = models.DateField(default=datetime.datetime.today)
    due_date = models.DateField(default=(datetime.datetime.today()+datetime.timedelta(days=7)))
    question = models.ManyToManyField(Question)
    
    def __unicode__(self):
        return self.name