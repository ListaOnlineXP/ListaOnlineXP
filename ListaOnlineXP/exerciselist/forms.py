# -*- coding: utf-8 -*-

from django import forms

class GetCodeForm(forms.Form):
    code = forms.CharField(max_length=1000, label='Código', widget=forms.Textarea(attrs={'class':'special'}) )
    test = forms.CharField(max_length=1000, label='Teste', widget=forms.Textarea(attrs={'class':'special'}) )

# not done
class MultipleChoiceQuestionAnswersForm(forms.Form):
    def __init__(self, *args, **kargs):
        label = 'x'
        lista = ([(1,1), (2,2)])
        super(MultipleChoiceQuestionAnswersForm, self).__init__(self, *args, **kargs)
        self.fields['answer'] = forms.ChoiceField(widget = forms.RadioSelect(), choices=lista, label=label)
