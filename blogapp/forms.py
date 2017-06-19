from django import forms
from django.contrib.auth.models import User

class NewBlogForm(forms.Form):
	name = forms.CharField(max_length=30)
	description = forms.CharField(max_length=4000)



