from django import forms

class NewStudentForm(forms.Form):

	name = forms.CharField(max_length=100)
	nusp = forms.CharField(max_length=100)
	passwd = forms.CharField(max_length=20, widget=forms.PasswordInput)

	def clean_nusp(self):
		nusp = self.cleaned_data['nusp']
		for char in nusp:
			if char not in [str(i) for i in range(0, 10)]:
				raise forms.ValidationError("NUSP invalido.")
		return nusp


class StudentLoginForm(forms.Form):

	nusp = forms.CharField(max_length=100)
	passwd = forms.CharField(max_length=20, widget=forms.PasswordInput)

	def clean_nusp(self):
		nusp = self.cleaned_data['nusp']
		for char in nusp:
			if char not in [str(i) for i in range(0, 10)]:
				raise forms.ValidationError("NUSP invalido.")
		return nusp
