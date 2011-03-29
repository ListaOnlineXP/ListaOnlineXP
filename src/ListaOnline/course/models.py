from django.db import models

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
        

    