# -*- coding: utf-8 -*-

from django import forms

class GetCodeForm(forms.Form):
    code = forms.CharField(max_length=1000, label='Código', widget=forms.Textarea(attrs={'class':'special'}) )
    test = forms.CharField(max_length=1000, label='Teste', widget=forms.Textarea(attrs={'class':'special'}) )

