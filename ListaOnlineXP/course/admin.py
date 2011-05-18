# -*- coding: utf-8 -*-

from django.contrib import admin
from authentication.models import Teacher
from models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    
admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher)
