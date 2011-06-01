# -*- coding: utf-8 -*-

from django import forms
from models import MultipleChoiceAlternative, MultipleChoiceQuestionAnswer, DiscursiveQuestionAnswer, JavaQuestionAnswer

class GetCodeForm(forms.Form):
    code = forms.CharField(max_length=1000, label='Código', widget=forms.Textarea(attrs={'class':'special'}) )
    test = forms.CharField(max_length=1000, label='Teste', widget=forms.Textarea(attrs={'class':'special'}) )


class MultipleChoiceAnswerModelForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(MultipleChoiceAnswerModelForm, self).__init__(*args, **kargs)
        self.fields['chosen_alternative'].queryset = self.instance.question_answered.casted().get_alternatives()
        self.fields['chosen_alternative'].empty_label=None
        self.fields['chosen_alternative'].label='Resposta'
        

    class Meta:
        model = MultipleChoiceQuestionAnswer
        exclude = ('type',)
        widgets = {
                'chosen_alternative': forms.RadioSelect(),
        }


class DiscursiveAnswerModelForm(forms.ModelForm):
    class Meta:
        model = DiscursiveQuestionAnswer
        fields = ('text',)


class JavaAnswerModelForm(forms.ModelForm):
    class Meta:
        model = JavaQuestionAnswer
        fields = ('code',)

