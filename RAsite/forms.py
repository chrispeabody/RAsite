from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	username = forms.CharField(max_length = 30)
	password = forms.CharField(widget = forms.PasswordInput)

	class Meta: 
		model = User
		fields = ['username','email','password']






