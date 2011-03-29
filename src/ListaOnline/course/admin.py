from django.contrib import admin
from ListaOnline.course.models import Course, Teacher, ExerciseList, Question, Answer

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher')
    
class ExerciseListAdmin(admin.ModelAdmin):
    filter_horizontal = ('question',)
    
admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher)
admin.site.register(ExerciseList, ExerciseListAdmin)
admin.site.register(Question)
admin.site.register(Answer)