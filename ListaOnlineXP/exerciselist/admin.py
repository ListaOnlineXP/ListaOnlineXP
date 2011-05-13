# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class ExerciseListAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)
    
class MultipleChoiceCorrectAlternativeInline(admin.StackedInline):
    model = MultipleChoiceCorrectAlternative
    
class MultipleChoiceWrongAlternativeInline(admin.StackedInline):
    model = MultipleChoiceWrongAlternative
    extra = 1
    
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [
        MultipleChoiceCorrectAlternativeInline,
        MultipleChoiceWrongAlternativeInline,
    ]

admin.site.register(ExerciseList, ExerciseListAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(JavaQuestion)
admin.site.register(DiscursiveQuestion)
