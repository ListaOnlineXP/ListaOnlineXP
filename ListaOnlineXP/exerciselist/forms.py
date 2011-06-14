# -*- coding: utf-8 -*-

from django import forms
from models import *

class MultipleChoiceAnswerForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(MultipleChoiceAnswerForm, self).__init__(*args, **kargs)
        self.fields['chosen_alternative'].queryset = self.instance.question_answered.casted().get_alternatives().order_by('?')
        self.fields['chosen_alternative'].empty_label='Em branco'
        self.fields['chosen_alternative'].label='Resposta'
        

    class Meta:
        model = MultipleChoiceAnswer
        exclude = ('type',)
        widgets = {
                'chosen_alternative': forms.RadioSelect(),
        }


class DiscursiveAnswerForm(forms.ModelForm):
    class Meta:
        model = DiscursiveAnswer
        fields = ('text',)


class JavaAnswerForm(forms.ModelForm):
    class Meta:
        model = JavaAnswer
        fields = ('code',)

class TrueFalseAnswerItemForm(forms.ModelForm):
    def __init__(self, *args, **kargs):
        super(TrueFalseAnswerItemForm, self).__init__(*args, **kargs)
        self.fields['given_answer'].label=self.instance.item_answered.text
    
    class Meta:
        model = TrueFalseAnswerItem
        fields = ('given_answer',)

class FileAnswerForm(forms.ModelForm):
    class Meta:
        model = FileAnswer
        fields = ('file', )



        
class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        exclude = ['type']


class DiscursiveQuestionForm(forms.ModelForm):
    class Meta:
        model = DiscursiveQuestion
        exclude = ['type']

class JavaQuestionForm(forms.ModelForm):
    class Meta:
        model = JavaQuestion
        exclude = ['type']
        
class TrueFalseQuestionItemForm(forms.ModelForm):
    class Meta:
        model = TrueFalseItem
        exclude = ['type']

class FileQuestionForm(forms.ModelForm):
    class Meta:
        model = FileQuestion
        exclude = ['type']


