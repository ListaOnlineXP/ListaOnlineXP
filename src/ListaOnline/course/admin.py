from django.contrib import admin
from ListaOnline.course.models import Course, Teacher, ExerciseList, MultipleChoiceQuestion, MultipleChoiceCorrectAnswer, MultipleChoiceWrongAnswer

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher')
    
class ExerciseListAdmin(admin.ModelAdmin):
    filter_horizontal = ('question',)
    
class MultipleChoiceCorrectAnswerInline(admin.StackedInline):
    model = MultipleChoiceCorrectAnswer
    
class MultipleChoiceWrongAnswerInline(admin.StackedInline):
    model = MultipleChoiceWrongAnswer
    extra = 1
    
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [
        MultipleChoiceCorrectAnswerInline,
        MultipleChoiceWrongAnswerInline,
    ]
    
admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher)
admin.site.register(ExerciseList, ExerciseListAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(MultipleChoiceCorrectAnswer)
admin.site.register(MultipleChoiceWrongAnswer)
