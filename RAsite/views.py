# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from .forms import UserForm
from .Spiders import ReviewSpider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

# This is what is used to call the spider you made and execute it
# One thing to look out for is how many times it adds to the database (Make sure correct amount of entries)
def crawl(request):
	runner = CrawlerRunner()

	d = runner.crawl(ReviewSpider)
	d.addBoth(lambda _: reactor.stop())
	reactor.run() # the script will block here until the crawling is finished
	redirect('/')

	return render(request, 'index.html')

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
