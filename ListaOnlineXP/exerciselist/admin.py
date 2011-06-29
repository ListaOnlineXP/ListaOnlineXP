from django.contrib import admin
from models import *
from django import forms


class QuestionExerciseInline(admin.StackedInline):
    model = ExerciseList.questions.through

class ExerciseListForm(forms.ModelForm):
    model = ExerciseList

    def clean(self):
        data = self.cleaned_data
 
        max_number_of_students = data["max_number_of_students"]
        min_number_of_students = data["min_number_of_students"]
        if max_number_of_students < min_number_of_students:
                raise forms.ValidationError("Max number of students is fewer than min number of students".format(max_number_of_students))
        return data


class ExerciseListAdmin(admin.ModelAdmin):
    model = ExerciseListQuestionThrough
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
        'tags'
    ]


class JavaQuestionAdmin(admin.ModelAdmin):
    fields = [
        'text',
        'criteria',
        'tags'
    ]


class DiscursiveQuestionAdmin(admin.ModelAdmin):
    fields = [ 
	    'text',
        'tags'
    ]


class TrueFalseItemInline(admin.StackedInline):
    model = TrueFalseItem


class TrueFalseQuestionAdmin(admin.ModelAdmin):
    inlines = [
        TrueFalseItemInline,
    ]
    fields = [
	    'text',
        'tags'
    ]


class ExerciseListSolutionAdmin(admin.ModelAdmin):
    fields = [
        'exercise_list',
        'chosen_topic',
    ]


class FileQuestionAdmin(admin.ModelAdmin):
    exclude = [
        'type',
    ]


admin.site.register(ExerciseList, ExerciseListAdmin, form=ExerciseListForm)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(JavaQuestion, JavaQuestionAdmin)
admin.site.register(DiscursiveQuestion, DiscursiveQuestionAdmin)
admin.site.register(TrueFalseQuestion, TrueFalseQuestionAdmin)
admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(ExerciseListSolution, ExerciseListSolutionAdmin)
admin.site.register(FileQuestion, FileQuestionAdmin)
