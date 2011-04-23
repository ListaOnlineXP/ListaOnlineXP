# -*- coding: utf-8 -*-

from django import forms

class SignUpForm(forms.Form):

    name = forms.CharField(max_length=100, label=u'Nome')
    username = forms.CharField(max_length=20, label=u'Nome de usuário')
    nusp = forms.CharField(max_length=100, label=u'Número USP')
    passwd = forms.CharField(max_length=20, widget=forms.PasswordInput, label=u'Senha')
    confirm_passwd = forms.CharField(max_length=20, widget=forms.PasswordInput, label=u'Confirmação de senha')

    def clean_nusp(self):
        nusp = self.cleaned_data['nusp']
        for char in nusp:
            if char not in [str(i) for i in range(0, 10)]:
                raise forms.ValidationError("NUSP inválido.")
        return nusp

    def clean(self):
        cleaned_data = self.cleaned_data
        passwd = cleaned_data.get('passwd', '')
        confirm_passwd = cleaned_data.get('confirm_passwd', '')
        if passwd and passwd != confirm_passwd:
            self._errors['confirm_passwd'] = self.error_class(["Confirmação de senha inválida."])
            del cleaned_data['confirm_passwd']
        return cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(max_length=20, label=u'Nome de usuario')
    passwd = forms.CharField(max_length=20, widget=forms.PasswordInput, label=u'Senha')

