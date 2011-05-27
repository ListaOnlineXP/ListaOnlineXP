# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory

from models import MultipleChoiceAlternative, DiscursiveQuestionAnswer

class GetCodeForm(forms.Form):
    code = forms.CharField(max_length=1000, label='Código', widget=forms.Textarea(attrs={'class':'special'}) )
    test = forms.CharField(max_length=1000, label='Teste', widget=forms.Textarea(attrs={'class':'special'}) )

#This form class makes forms given a question. If queries the question for its alternatives, and populates itself with it. The trick is on the __init__ method. It adds a input parameter(multiple_choice_question) to the MultipleChoiceQuestionForm. With it, it overwrites the alternative field's queryset parameter with the proper queryset. Once it's done, it returns a form with the correct alternatives for a question.
class MultipleChoiceQuestionForm(forms.Form):
    alternative = forms.ModelChoiceField(queryset=MultipleChoiceAlternative.objects.none(), widget = forms.RadioSelect(), empty_label=None, label='Resposta')

    def __init__(self, *args, **kargs):
        multiple_choice_question = kargs.pop('multiple_choice_question')
        finalized = kargs.pop('finalized')
        super(MultipleChoiceQuestionForm, self).__init__(*args, **kargs)
        self.fields['alternative'].queryset = multiple_choice_question.get_alternatives() 
        if finalized:
            self.fields['alternative'].widget.attrs['disabled'] = 'disabled'

class DiscursiveQuestionForm(forms.Form):
    discursive_answer = forms.CharField(label='Resposta', widget=forms.Textarea)

    def __init__(self, *args, **kargs):
        finalized = kargs.pop('finalized')
        super(DiscursiveQuestionForm, self).__init__(*args, **kargs)
        if finalized:
            self.fields['discursive_answer'].widget.attrs['disabled'] = 'disabled'


class JavaQuestionForm(forms.Form):
    java_answer = forms.CharField(label='Resposta', widget=forms.Textarea)

    def __init__(self, *args, **kargs):
        finalized = kargs.pop('finalized')
        super(JavaQuestionForm, self).__init__(*args, **kargs)
        if finalized:
            self.fields['java_answer'].widget.attrs['disabled'] = 'disabled'


class TrueFalseQuestionForm(forms.ModelForm):
    pass

class DiscursiveQuestionAnswerModelForm(forms.ModelForm):
    class Meta:
        model = DiscursiveQuestionAnswer


