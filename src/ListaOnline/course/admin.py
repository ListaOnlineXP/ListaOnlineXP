from django.contrib import admin
from ListaOnline.course.models import Course, Teacher, ExerciseList, MultipleChoiceQuestion, MultipleChoiceAnswer

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher')
    
class ExerciseListAdmin(admin.ModelAdmin):
    filter_horizontal = ('question',)
    
class MultipleChoiceAnswerInline(admin.StackedInline):
    model = MultipleChoiceAnswer
    
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [
        MultipleChoiceAnswerInline,
    ]
    
admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher)
admin.site.register(ExerciseList, ExerciseListAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(MultipleChoiceAnswer)
