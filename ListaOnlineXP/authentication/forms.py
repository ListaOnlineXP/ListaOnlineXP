# -*- coding: utf-8 -*-

from django import forms
from django.contrib import auth
from models import Profile


class SignUpForm(forms.Form):

    first_name = forms.CharField(max_length=100, label=u'Nome')
    last_name = forms.CharField(max_length=100, label=u'Sobrenome')
    email = forms.EmailField(max_length=100, label=u'E-mail')
    username = forms.CharField(max_length=20, label=u'Nome de usuário')
    passwd = forms.CharField(max_length=20, widget=forms.PasswordInput,
                             label=u'Senha')
    confirm_passwd = forms.CharField(max_length=20, widget=forms.PasswordInput,
                                     label=u'Confirmação de senha')

    def clean(self):
        cleaned_data = self.cleaned_data
        passwd = cleaned_data.get('passwd', '')
        confirm_passwd = cleaned_data.get('confirm_passwd', '')
        if passwd and confirm_passwd and passwd != confirm_passwd:
            self._errors['confirm_passwd'] = self.error_class(
                ["Confirmação de senha inválida."]
            )
            del cleaned_data['confirm_passwd']
        return cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(max_length=20, label=u'Usuário')
    passwd = forms.CharField(max_length=20, widget=forms.PasswordInput,
                             label=u'Senha')

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username', '')
        passwd = cleaned_data.get('passwd', '')
        user = auth.authenticate(username=username, password=passwd)
        if user is None:
            raise forms.ValidationError(u'Usuário ou senha incorreta.')
        try:
            profile = Profile.objects.get(user=user)
        except:
            raise forms.ValidationError(u'Usuário não é um estudante '
                                        u'ou professor do sistema.')
        return cleaned_data
