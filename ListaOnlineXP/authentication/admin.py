# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Student


class StudentAdmin(admin.ModelAdmin):
    fields = ('name', 'nusp', 'courses')

admin.site.register(Student, StudentAdmin)
