
from django.contrib import admin
from models import *
from django import forms

class QuestionExerciseInline(admin.StackedInline): 
    model = ExerciseList.questions.through

#Sortable inline, based on: http://djangosnippets.org/snippets/1053/
class ExerciseListForm(forms.ModelForm):
    model = ExerciseList
    class Media:
        js = (
            '/site_media/js/custom_admin_jquery.js',
            '/site_media/js/custom_admin_jquery_ui.js',
            '/site_media/js/exerciselist_sort.js',
        )

class ExerciseListAdmin(admin.ModelAdmin):
    model = ExerciseListQuestionThrough;

    inlines = [
            QuestionExerciseInline,
    ]

    exclude = ('questions',)

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


admin.site.register(ExerciseList, ExerciseListAdmin, form=ExerciseListForm)
#admin.site.register(ExerciseListSolution)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(JavaQuestion)
admin.site.register(DiscursiveQuestion)
#admin.site.register(MultipleChoiceQuestionAnswer)
#admin.site.register(JavaQuestionAnswer)
#admin.site.register(DiscursiveQuestionAnswer)
