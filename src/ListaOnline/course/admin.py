from django.contrib import admin
from ListaOnline.course.models import Course, Teacher

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher')
    
admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher)