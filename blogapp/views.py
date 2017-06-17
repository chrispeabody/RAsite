from django.shortcuts import render
from django.http import HttpResponseRedirect
from blogapp.models import Test
from blogapp.forms import NewBlogForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import UserForm

		
# Create your views here.
def index(request):
	Blog = Test.objects.all()
	return render(request, 'blogs.html', { 'blogs': Blog })

def newblog(request):
	return render(request, 'newblog.html')

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

	
		
	return	redirect('/')

def getNewBlogData(request):
	if request.method == 'POST':
		form = NewBlogForm(request.POST)

		if form.is_valid():
			ourname = request.POST.get('name', '')
			ourdescription = request.POST.get('description', '')

			t = Test(name = ourname, description = ourdescription)
			t.save()

	return HttpResponseRedirect('/blogapp/new')
	# return render(request, 'newblog.html')
