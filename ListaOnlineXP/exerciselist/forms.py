# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory

from exerciselist.models import MultipleChoiceQuestionAnswer, MultipleChoiceAlternative

class GetCodeForm(forms.Form):
    code = forms.CharField(max_length=1000, label='Código', widget=forms.Textarea(attrs={'class':'special'}) )
    test = forms.CharField(max_length=1000, label='Teste', widget=forms.Textarea(attrs={'class':'special'}) )

# not done
#class MultipleChoiceQuestionAnswersForm(forms.Form):
#    def __init__(self, *args, **kargs):
#        label = 'x'
#        lista = ([(1,1), (2,2)])
#        super(MultipleChoiceQuestionAnswersForm, self).__init__(self, *args, **kargs)
#        self.fields['answer'] = forms.ChoiceField(widget = forms.RadioSelect(), choices=lista, label=label)


class MultipleChoiceQuestionAnswerForm(forms.Form):
    alternative = forms.ModelChoiceField(queryset=MultipleChoiceAlternative.objects.none())

    def __init__(self, *args, **kargs):
        multiple_choice_question = kargs.pop('multiple_choice_question')
        super(MultipleChoiceQuestionAnswerForm, self).__init__(*args, **kargs)
        self.fields['alternative'].queryset = multiple_choice_question.get_alternatives() 
