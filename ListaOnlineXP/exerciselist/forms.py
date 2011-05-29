# -*- coding: utf-8 -*-

from django import forms
from models import MultipleChoiceAlternative, MultipleChoiceQuestionAnswer, MultipleChoiceWrongAlternative, MultipleChoiceCorrectAlternative

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


class MultipleChoiceAnswerForm(forms.Form):
    alternative = forms.ModelChoiceField(queryset=MultipleChoiceAlternative.objects.none(), widget = forms.RadioSelect(), empty_label=None, label='Resposta')

    def __init__(self, *args, **kargs):

        if 'instance' in kargs:
            multiple_choice_answer = kargs.pop('instance')
        else: 
            raise ValueError('No instance given to form')

        if 'finalized' in kargs:
            finalized = kargs.pop('finalized')
        else:
            finalized = False

        

        super(MultipleChoiceAnswerForm, self).__init__(*args, **kargs)
        self.fields['alternative'].queryset = multiple_choice_answer.question_answered.casted().get_alternatives()

        #If received data (as in request.POST)
        #if self.data:
        #    if self.prefix:
        #    else:
        #        raise ValueError('No prefix given. It is needed to associate POST data to model')


        if finalized:
            self.fields['alternative'].widget.attrs['disabled'] = 'disabled'

class DiscursiveAnswerForm(forms.Form):
    discursive_answer = forms.CharField(label='Resposta', widget=forms.Textarea)

    def __init__(self, *args, **kargs):
        
        if 'instance' in kargs:
            discursive_answer = kargs.pop('instance')
        else: 
            raise ValueError('No instance given to form')

        if 'finalized' in kargs:
            finalized = kargs.pop('finalized')
        else:
            finalized = False

        super(DiscursiveQuestionForm, self).__init__(*args, **kargs)
        if finalized:
            self.fields['discursive_answer'].widget.attrs['disabled'] = 'disabled'


class JavaAnswerForm(forms.Form):
    java_answer = forms.CharField(label='Resposta', widget=forms.Textarea)

    def __init__(self, *args, **kargs):

        if 'instance' in kargs:
            java_answer = kargs.pop('instance')
        else: 
            raise ValueError('No instance given to form')

        if 'finalized' in kargs:
            finalized = kargs.pop('finalized')
        else:
            finalized = False

        super(DiscursiveQuestionForm, self).__init__(*args, **kargs)
        if finalized:
            self.fields['discursive_answer'].widget.attrs['disabled'] = 'disabled'



class TrueFalseQuestionForm(forms.ModelForm):
    pass

