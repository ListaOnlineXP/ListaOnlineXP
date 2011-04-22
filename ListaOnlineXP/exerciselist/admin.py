# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class ExerciseListAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)
    
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

admin.site.register(ExerciseList, ExerciseListAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(JavaQuestion)

