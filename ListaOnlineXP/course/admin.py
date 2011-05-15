# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Course, CourseMember


class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name') 


class CourseMemberAdmin(admin.ModelAdmin):
    fields = ('course', 'profile', 'role')
    

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseMember, CourseMemberAdmin)
