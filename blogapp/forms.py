from django import forms

class NewBlogForm(forms.Form):
	name = forms.CharField(max_length=30)
	description = forms.CharField(max_length=4000)