from django.http import HttpResponseRedirect
from blogapp.models import Test
from blogapp.forms import NewBlogForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
		
# Create your views here.
def index(request):
	Blog = Test.objects.all()
	return render(request, 'blogs.html', { 'blogs': Blog })

def newblog(request):
	return render(request, 'newblog.html')

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
