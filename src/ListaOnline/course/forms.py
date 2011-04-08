# -*- coding: utf-8 -*-
from django import forms

class NewStudentForm(forms.Form):

	name = forms.CharField(max_length=100)
	username = forms.CharField(max_length=20, label='Nome de usuario')
	nusp = forms.CharField(max_length=100)
	passwd = forms.CharField(max_length=20, widget=forms.PasswordInput)
	confirm_passwd = forms.CharField(max_length=20, widget=forms.PasswordInput)

	def clean_nusp(self):
		nusp = self.cleaned_data['nusp']
		for char in nusp:
			if char not in [str(i) for i in range(0, 10)]:
				raise forms.ValidationError("NUSP invalido.")
		return nusp

	def clean(self):
		cleaned_data = self.cleaned_data
		passwd = cleaned_data['passwd']
		confirm_passwd = cleaned_data['confirm_passwd']
		if passwd != confirm_passwd:
			self._errors['confirm_passwd'] = self.error_class(["Confirmacao de senha invalida."])
			del cleaned_data['confirm_passwd']
		return cleaned_data


class StudentLoginForm(forms.Form):

	username = forms.CharField(max_length=20, label='Nome de usuario')
	passwd = forms.CharField(max_length=20, widget=forms.PasswordInput)

class GetCodeForm(forms.Form):
    
    code = forms.CharField(max_length=1000, label='Código', widget=forms.Textarea)
    test = forms.CharField(max_length=1000, label='Teste', widget=forms.Textarea)
    