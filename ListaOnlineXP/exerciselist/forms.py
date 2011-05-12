# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory

from models import MultipleChoiceAlternative

class GetCodeForm(forms.Form):
    code = forms.CharField(max_length=1000, label='Código', widget=forms.Textarea(attrs={'class':'special'}) )
    test = forms.CharField(max_length=1000, label='Teste', widget=forms.Textarea(attrs={'class':'special'}) )

class MultipleChoiceQuestionForm(forms.Form):
    alternative = forms.ModelChoiceField(queryset=MultipleChoiceAlternative.objects.none(), widget = forms.RadioSelect(), empty_label=None, label='Resposta')

    def __init__(self, *args, **kargs):
        multiple_choice_question = kargs.pop('multiple_choice_question')
        super(MultipleChoiceQuestionForm, self).__init__(*args, **kargs)
        self.fields['alternative'].queryset = multiple_choice_question.get_alternatives() 
