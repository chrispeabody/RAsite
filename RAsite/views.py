# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import UserForm

def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

######################
### ACCOUNT SYSTEM ###
######################

def registerForm(request):
    return render(request, 'registration.html')

def logginginForm(request):
	return render(request, 'login.html')

def registerUser(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		
		if form.is_valid():
			user = form.save(commit=False)

			username = request.POST.get('username','')
			password = request.POST.get('password','')
			user.set_password(password)
			user.save()

			user = authenticate(username = username, password = password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('/')
			
		return	redirect('/blogapp/registerForm')

			
def loggingout(request):	
	logout(request)	
	return	redirect('/')

def loggingin(request):
	if request.method == 'POST':
		form = UserForm(request.POST)

		username = request.POST.get('username','')
		password = request.POST.get('password','')

		user = authenticate(username = username, password = password)


		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('/')
