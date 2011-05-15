# -*- coding: utf-8 -*-

from django.db import models
from authentication.models import Profile


class Course(models.Model):
    
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True)

    def __unicode__(self):
        return '(' + self.code + ') ' + self.name 

    def link(self):
        return '/course/%s' % self.id
    
    def enroll_link(self):
        return '/course/enroll/%s' % self.id


class CourseMember(models.Model):
    
    restrict = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course)
    profile = models.ForeignKey(Profile)
    role = models.CharField(max_length=1, choices=(
        ('S', 'Student'),
        ('T', 'Teacher'),
    ))

    def save(self):
        # força uma chave primária com as 3 colunas: course, profile e role
        self.restrict = '%s,%s,%s' % (self.course.id, self.profile.id,
                                      self.role)
        super(CourseMember, self).save()

    def __unicode__(self):
        return '%s - %s' % (unicode(self.course), unicode(self.profile))

    @classmethod
    def is_member_of_course(cls, profile, course, role=None):
        member = CourseMember.objects.filter(profile=profile, course=course)
        if role is not None:
            member.filter(role=role)
        if member.count() > 0:
            return True
        return False

    @classmethod
    def is_teacher_of_course(cls, profile, course):
        return cls.is_member_of_course(profile, course, 'T')

    @classmethod
    def is_student_of_course(cls, profile, course):
        return cls.is_member_of_course(profile, course, 'S')
