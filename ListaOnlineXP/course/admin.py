# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Course, Teacher, Student


class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher')
    
class StudentAdmin(admin.ModelAdmin):
    fields = ('name', 'nusp', 'courses')

admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher)
admin.site.register(Student, StudentAdmin)
