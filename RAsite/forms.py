from django import forms
from django.contrib.auth.models import User
from CSPtool.models import CSP

class UserForm(forms.ModelForm):
	username = forms.CharField(max_length = 30)
	password = forms.CharField(widget = forms.PasswordInput)

	class Meta: 
		model = User
		fields = ['username','email','password']

class newReviewForm(forms.ModelForm):
	cspname = forms.ModelChoiceField(queryset = CSP.objects.all(), empty_label=None)
	cspname.widget.attrs['class'] = 'form-control'
	reviewtext = forms.CharField(max_length = 2000)

	class Meta:
		model = CSP
		fields = ['cspname','reviewtext']

class netInfoForm(forms.ModelForm):
	# Current csp the user uses
	currcsp = forms.ModelChoiceField(queryset = CSP.objects.all(), empty_label=None)
	currcsp.widget.attrs['class'] = 'form-control'

	# Review, if the user has one
	reviewtext = forms.CharField(max_length = 2000)

	# What type of service they need
	typ = [(0, 'Infrustructure as a Service'),
			(1, 'Platform as a Service'),
			(2, 'Software as a Service')]

	serviceType = forms.ChoiceField(choices = typ)
	serviceType.widget.attrs['class'] = 'form-control'

	# ----------------------------------------------------- #
	# The user's preference for importance of these aspects #
	# ----------------------------------------------------- #

	chs = [(0, 'No preference'),
			(1, 'Low importance'),
			(2, 'Moderate importance'),
			(3, 'High importance')]

	# Physical Infrastructure
	prefPhysInfra = forms.ChoiceField(choices = chs)
	prefPhysInfra.widget.attrs['class'] = 'form-control'

	# Networking
	prefNet = forms.ChoiceField(choices = chs)
	prefNet.widget.attrs['class'] = 'form-control'

	# Computation
	prefComp = forms.ChoiceField(choices = chs)
	prefComp.widget.attrs['class'] = 'form-control'

	# Storage
	prefStorage = forms.ChoiceField(choices = chs)
	prefStorage.widget.attrs['class'] = 'form-control'

	# Apps on the platform
	prefPlatApps = forms.ChoiceField(choices = chs)
	prefPlatApps.widget.attrs['class'] = 'form-control'

	# Data Security
	prefData = forms.ChoiceField(choices = chs)
	prefData.widget.attrs['class'] = 'form-control'

	class Meta:
		model = CSP
		fields = ['currcsp',
				'reviewtext',
				'serviceType',
				'prefPhysInfra',
				'prefNet',
				'prefComp',
				'prefStorage',
				'prefPlatApps',
				'prefData']





