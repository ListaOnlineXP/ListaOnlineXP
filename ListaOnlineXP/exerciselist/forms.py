# -*- coding: utf-8 -*-

from django import forms
from models import *

class MultipleChoiceAnswerForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(MultipleChoiceAnswerForm, self).__init__(*args, **kargs)
        self.fields['chosen_alternative'].queryset = self.instance.question_answered.casted().get_alternatives().order_by('?')
        self.fields['chosen_alternative'].empty_label=None
        self.fields['chosen_alternative'].label='Resposta'
        

    class Meta:
        model = MultipleChoiceAnswer
        exclude = ('type', 'score', 'comment')
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

class TopicsChoiceForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(TopicsChoiceForm, self).__init__(*args, **kargs)
        self.fields['chosen_topic'].queryset = self.instance.exercise_list.topics.order_by('name')
        self.fields['chosen_topic'].empty_label=None
        self.fields['chosen_topic'].label='Escolha um tema:'


    class Meta:
        model = ExerciseListSolution
        fields = ('chosen_topic',)
        widgets = {
            'chosen_topic': forms.RadioSelect(),
    }


#===Begin Exercise list creation forms===

class ExerciseListForm(forms.ModelForm):
    class Meta:
        model = ExerciseList
        exclude=['questions']

    def __init__(self, *args, **kargs):
        super(ExerciseListForm, self).__init__(*args, **kargs)
        self.fields['course'].empty_label=None
        

class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        exclude = ['type', 'tags']

class MultipleChoiceCorrectAlternativeForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceCorrectAlternative
        exclude = ['question']

    def __init__(self, *args, **kargs):
        super(MultipleChoiceCorrectAlternativeForm, self).__init__(*args, **kargs)
        self.fields['text'].label = 'Alternativa correta'

class MultipleChoiceWrongAlternativeForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceWrongAlternative
        exclude = ['question']
    def __init__(self, *args, **kargs):
        super(MultipleChoiceWrongAlternativeForm, self).__init__(*args, **kargs)
        self.fields['text'].label = 'Alternativa incorreta'

class DiscursiveQuestionForm(forms.ModelForm):
    class Meta:
        model = DiscursiveQuestion
        exclude = ['type', 'tags']

class JavaQuestionForm(forms.ModelForm):
    class Meta:
        model = JavaQuestion
        exclude = ['type', 'tags']

class TrueFalseQuestionForm(forms.ModelForm):
    class Meta:
        model = TrueFalseQuestion
        exclude = ['type', 'tags']

class TrueFalseQuestionItemForm(forms.ModelForm):
    class Meta:
        model = TrueFalseItem
        exclude = ['question']
        widgets = {'text' : forms.TextInput}

class FileQuestionForm(forms.ModelForm):
    class Meta:
        model = FileQuestion
        exclude = ['type', 'tags']

class DeleteObjectForm(forms.Form):
    delete = forms.BooleanField(required=False, label='Apagar questão')

class OrderForm(forms.Form):
    order = forms.IntegerField(widget=forms.HiddenInput)

class WeightForm(forms.Form):
    weight = forms.IntegerField(min_value=1, label='Peso')
    
#===END Exercise list creation forms===


class AnswerCorrectForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('score', 'comment',)
