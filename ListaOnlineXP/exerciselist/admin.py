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
    fields = [
	    'text',
	    'weight',
    ]

class JavaQuestionAdmin(admin.ModelAdmin):
    fields = [
	    'text',
	    'weight',
	    'criteria',
    ]

class DiscursiveQuestionAdmin(admin.ModelAdmin):
    fields = [
	    'text',
	    'weight',
    ]

class TrueFalseItemInline(admin.StackedInline):
    model = TrueFalseItem

class TrueFalseQuestionAdmin(admin.ModelAdmin):
    inlines = [
        TrueFalseItemInline,
    ]
    fields = [
	    'text',
	    'weight',
    ]

admin.site.register(ExerciseList, ExerciseListAdmin, form=ExerciseListForm)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(JavaQuestion, JavaQuestionAdmin)
admin.site.register(DiscursiveQuestion, DiscursiveQuestionAdmin)
admin.site.register(TrueFalseQuestion, TrueFalseQuestionAdmin)
#admin.site.register(MultipleChoiceQuestionAnswer)
#admin.site.register(ExerciseListSolution)
#admin.site.register(JavaQuestionAnswer)
#admin.site.register(DiscursiveQuestionAnswer)
