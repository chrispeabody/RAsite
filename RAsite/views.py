# Site imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from .forms import UserForm, newReviewForm, netInfoForm
from CSPtool.models import CSP, Review, Rating, CatScore
from datetime import datetime

# Crawler imports
from .Spiders import ReviewSpider, updateAverages
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from crochet import setup
setup()

# Bayes network imports
from bayesian.bbn import build_bbn

from .graphCalc import userQoE, networkQoS, cloudSecurity, cost, bayes
import random
random.seed()

#####################
### PAGE REQUESTS ###
#####################

def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def tutorial(request):
	return render(request, 'tutorial.html')

#####################
### FUNC REQUESTS ###
#####################

# used for setting up tables with hardcoded values
# useful for if we flush
# Only run after aggReviews
def initTables(request):
	csp = CSP.objects.get(name='Amazon Web Services')
	CatScore(CSP=csp, type='support', value=0.95).save()
	CatScore(CSP=csp, type='computing', value=0.99).save()
	CatScore(CSP=csp, type='security', value=1.0).save()
	CatScore(CSP=csp, type='performance', value=0.96).save()

	csp = CSP.objects.get(name='Microsoft Azure')
	CatScore(CSP=csp, type='support', value=0.93).save()
	CatScore(CSP=csp, type='computing', value=0.99).save()
	CatScore(CSP=csp, type='security', value=0.96).save()
	CatScore(CSP=csp, type='performance', value=0.95).save()

	csp = CSP.objects.get(name='Google Cloud Platform')
	CatScore(CSP=csp, type='support', value=0.9).save()
	CatScore(CSP=csp, type='computing', value=0.92).save()
	CatScore(CSP=csp, type='security', value=0.96).save()
	CatScore(CSP=csp, type='performance', value=0.95).save()

	csp = CSP.objects.get(name='IBM Cloud')
	CatScore(CSP=csp, type='support', value=0.91).save()
	CatScore(CSP=csp, type='computing', value=0.97).save()
	CatScore(CSP=csp, type='security', value=0.94).save()
	CatScore(CSP=csp, type='performance', value=0.94).save()

	csp = CSP.objects.get(name='Rackspace')
	CatScore(CSP=csp, type='support', value=0.98).save()
	CatScore(CSP=csp, type='computing', value=0.84).save()
	CatScore(CSP=csp, type='security', value=0.9).save()
	CatScore(CSP=csp, type='performance', value=0.9).save()

	CtrlGrpWeight(ctrlGroup = 'AIS', domain = 'physical', weight = 0.25).save()
	CtrlGrpWeight(ctrlGroup = 'AIS', domain = 'network', weight = 0.75).save()
	CtrlGrpWeight(ctrlGroup = 'AIS', domain = 'compute', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'AIS', domain = 'storage', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'AIS', domain = 'app', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'AIS', domain = 'data', weight = 1).save()

	CtrlGrpWeight(ctrlGroup = 'AAC', domain = 'physical', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'AAC', domain = 'network', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'AAC', domain = 'compute', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'AAC', domain = 'storage', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'AAC', domain = 'app', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'AAC', domain = 'data', weight = 1).save()

	CtrlGrpWeight(ctrlGroup = 'BCR', domain = 'physical', weight = 0.73).save()
	CtrlGrpWeight(ctrlGroup = 'BCR', domain = 'network', weight = 0.64).save()
	CtrlGrpWeight(ctrlGroup = 'BCR', domain = 'compute', weight = 0.64).save()
	CtrlGrpWeight(ctrlGroup = 'BCR', domain = 'storage', weight = 0.64).save()
	CtrlGrpWeight(ctrlGroup = 'BCR', domain = 'app', weight = 0.55).save()
	CtrlGrpWeight(ctrlGroup = 'BCR', domain = 'data', weight = 0.64).save()

	CtrlGrpWeight(ctrlGroup = 'CCC', domain = 'physical', weight = 0.2).save()
	CtrlGrpWeight(ctrlGroup = 'CCC', domain = 'network', weight = 0.2).save()
	CtrlGrpWeight(ctrlGroup = 'CCC', domain = 'compute', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'CCC', domain = 'storage', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'CCC', domain = 'app', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'CCC', domain = 'data', weight = 0.8).save()

	CtrlGrpWeight(ctrlGroup = 'DSI', domain = 'physical', weight = 0).save()
	CtrlGrpWeight(ctrlGroup = 'DSI', domain = 'network', weight = 0.14).save()
	CtrlGrpWeight(ctrlGroup = 'DSI', domain = 'compute', weight = 0.71).save()
	CtrlGrpWeight(ctrlGroup = 'DSI', domain = 'storage', weight = 0.86).save()
	CtrlGrpWeight(ctrlGroup = 'DSI', domain = 'app', weight = 0.86).save()
	CtrlGrpWeight(ctrlGroup = 'DSI', domain = 'data', weight = 1).save()

	CtrlGrpWeight(ctrlGroup = 'DCS', domain = 'physical', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'DCS', domain = 'network', weight = 0.44).save()
	CtrlGrpWeight(ctrlGroup = 'DCS', domain = 'compute', weight = 0.44).save()
	CtrlGrpWeight(ctrlGroup = 'DCS', domain = 'storage', weight = 0.56).save()
	CtrlGrpWeight(ctrlGroup = 'DCS', domain = 'app', weight = 0.33).save()
	CtrlGrpWeight(ctrlGroup = 'DCS', domain = 'data', weight = 0.33).save()

	CtrlGrpWeight(ctrlGroup = 'EKM', domain = 'physical', weight = 0).save()
	CtrlGrpWeight(ctrlGroup = 'EKM', domain = 'network', weight = 0.75).save()
	CtrlGrpWeight(ctrlGroup = 'EKM', domain = 'compute', weight = 0.25).save()
	CtrlGrpWeight(ctrlGroup = 'EKM', domain = 'storage', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'EKM', domain = 'app', weight = 0.75).save()
	CtrlGrpWeight(ctrlGroup = 'EKM', domain = 'data', weight = 1).save()

	CtrlGrpWeight(ctrlGroup = 'GRM', domain = 'physical', weight = 0.46).save()
	CtrlGrpWeight(ctrlGroup = 'GRM', domain = 'network', weight = 0.46).save()
	CtrlGrpWeight(ctrlGroup = 'GRM', domain = 'compute', weight = 0.55).save()
	CtrlGrpWeight(ctrlGroup = 'GRM', domain = 'storage', weight = 0.55).save()
	CtrlGrpWeight(ctrlGroup = 'GRM', domain = 'app', weight = 0.55).save()
	CtrlGrpWeight(ctrlGroup = 'GRM', domain = 'data', weight = 0.55).save()

	CtrlGrpWeight(ctrlGroup = 'HRS', domain = 'physical', weight = 0.64).save()
	CtrlGrpWeight(ctrlGroup = 'HRS', domain = 'network', weight = 0.55).save()
	CtrlGrpWeight(ctrlGroup = 'HRS', domain = 'compute', weight = 0.55).save()
	CtrlGrpWeight(ctrlGroup = 'HRS', domain = 'storage', weight = 0.55).save()
	CtrlGrpWeight(ctrlGroup = 'HRS', domain = 'app', weight = 0.64).save()
	CtrlGrpWeight(ctrlGroup = 'HRS', domain = 'data', weight = 0.91).save()

	CtrlGrpWeight(ctrlGroup = 'IAM', domain = 'physical', weight = 0.62).save()
	CtrlGrpWeight(ctrlGroup = 'IAM', domain = 'network', weight = 0.69).save()
	CtrlGrpWeight(ctrlGroup = 'IAM', domain = 'compute', weight = 0.85).save()
	CtrlGrpWeight(ctrlGroup = 'IAM', domain = 'storage', weight = 0.85).save()
	CtrlGrpWeight(ctrlGroup = 'IAM', domain = 'app', weight = 0.92).save()
	CtrlGrpWeight(ctrlGroup = 'IAM', domain = 'data', weight = 0.85).save()

	CtrlGrpWeight(ctrlGroup = 'IVS', domain = 'physical', weight = 0.54).save()
	CtrlGrpWeight(ctrlGroup = 'IVS', domain = 'network', weight = 0.77).save()
	CtrlGrpWeight(ctrlGroup = 'IVS', domain = 'compute', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'IVS', domain = 'storage', weight = 0.69).save()
	CtrlGrpWeight(ctrlGroup = 'IVS', domain = 'app', weight = 0.69).save()
	CtrlGrpWeight(ctrlGroup = 'IVS', domain = 'data', weight = 0.69).save()

	CtrlGrpWeight(ctrlGroup = 'IPY', domain = 'physical', weight = 0.2).save()
	CtrlGrpWeight(ctrlGroup = 'IPY', domain = 'network', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'IPY', domain = 'compute', weight = 0.8).save()
	CtrlGrpWeight(ctrlGroup = 'IPY', domain = 'storage', weight = 0.8).save()
	CtrlGrpWeight(ctrlGroup = 'IPY', domain = 'app', weight = 0.8).save()
	CtrlGrpWeight(ctrlGroup = 'IPY', domain = 'data', weight = 0.8).save()

	CtrlGrpWeight(ctrlGroup = 'MOS', domain = 'physical', weight = 0.4).save()
	CtrlGrpWeight(ctrlGroup = 'MOS', domain = 'network', weight = 0.25).save()
	CtrlGrpWeight(ctrlGroup = 'MOS', domain = 'compute', weight = 0.4).save()
	CtrlGrpWeight(ctrlGroup = 'MOS', domain = 'storage', weight = 0.15).save()
	CtrlGrpWeight(ctrlGroup = 'MOS', domain = 'app', weight = 0.65).save()
	CtrlGrpWeight(ctrlGroup = 'MOS', domain = 'data', weight = 0.35).save()

	CtrlGrpWeight(ctrlGroup = 'SEF', domain = 'physical', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'SEF', domain = 'network', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'SEF', domain = 'compute', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'SEF', domain = 'storage', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'SEF', domain = 'app', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'SEF', domain = 'data', weight = 1).save()

	CtrlGrpWeight(ctrlGroup = 'STA', domain = 'physical', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'STA', domain = 'network', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'STA', domain = 'compute', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'STA', domain = 'storage', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'STA', domain = 'app', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'STA', domain = 'data', weight = 1).save()

	CtrlGrpWeight(ctrlGroup = 'TVM', domain = 'physical', weight = 0).save()
	CtrlGrpWeight(ctrlGroup = 'TVM', domain = 'network', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'TVM', domain = 'compute', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'TVM', domain = 'storage', weight = 0.67).save()
	CtrlGrpWeight(ctrlGroup = 'TVM', domain = 'app', weight = 1).save()
	CtrlGrpWeight(ctrlGroup = 'TVM', domain = 'data', weight = 0.33).save()

	return render(request, 'index.html')


# For submitting new reviews
def addReview(request):
	if request.method == 'POST':
		form = newReviewForm(request.POST)

		if form.is_valid():
			cspname = form.cleaned_data['cspname']
			csp = CSP.objects.get(name = cspname)
			reviewtext = form.cleaned_data['reviewtext']

			rightnow = datetime.today().date()
			rev = Review(CSP = csp, plaintext = reviewtext, dateMade = rightnow)
			rev.save()

			updateAverages()

	else:
		form = newReviewForm()

	return render(request, 'newreview.html', {'form': form})

# Form for filling out all information you need
# for the bayes net to run properly
def getScore(request):
	if request.method == 'POST':
		form = netInfoForm(request.POST)

		if form.is_valid():
			# First, if the user had a review, add to database
			reviewtext = form.cleaned_data['reviewtext']
			if len(reviewtext) > 0:
				cspname = form.cleaned_data['currcsp']
				csp = CSP.objects.get(name = cspname)
	
				rightnow = datetime.today().date()
				rev = Review(CSP = csp, plaintext = reviewtext, dateMade = rightnow)
				rev.save()

				updateAverages()

			cspList = CSP.objects.all()
			chartDict = {}
			for csp in cspList:
				chartDict[csp.name] = results(csp.name, form.cleaned_data['serviceType'])

			# Here is where the magic will happen.
			chartInfo = results(form.cleaned_data['currcsp'], form.cleaned_data['serviceType'])
			return render(request, 'results.html', chartInfo)

	else:
		form = netInfoForm()

		return render(request, 'infoform.html', {'form': form})

# Experimenting with matrices
def results(cspname, serviceType):
	# Calculates user quality of experience
	uQoE, qoeMat = userQoE(cspname)
	nQoS, qosMat = networkQoS()
	cSec, secMat = cloudSecurity()
	cst, costMat = cost(serviceType)

	# average the nodes for now
	trust = bayes(0.5, uQoE, nQoS, cSec, cst)

	print("TRUST: ")
	print(trust)

	print("uQoe: ")
	print(uQoE)

	print("nQoS: ")
	print(nQoS)

	print("cSec: ")
	print(cSec)

	print("cst: ")
	print(cst)

	chartInfo = {
		'trust':trust,

		'cost':costMat[13, 13],
		'iaas':costMat[10, 13],
		'paas':costMat[11, 13],
		'saas':costMat[12, 13],
		'numCores':costMat[3, 10],
		'diskIO':costMat[4, 10],
		'storeSize':costMat[5, 10],
		'OS':costMat[6, 10],
		'bandwidth':costMat[7, 11],
 		'tieredBased':costMat[9, 12],
		'dataConsumed':costMat[0, 8],
		'transProc':costMat[1, 8],
		'APIreq':costMat[2, 8],

		'QoE':qoeMat[6, 6],
		'starRating':qoeMat[4, 6],
		'reviews':qoeMat[5, 6],
		'support':qoeMat[0, 4],
		'computing':qoeMat[1, 4],
		'security':qoeMat[2, 4],
		'performance':qoeMat[3, 4],

		'cloudSec':secMat[18, 18],
		'STARscore':secMat[16, 18],
		'controlGrps':secMat[17, 18],
		'AAC':secMat[0, 17],
		'IAM':secMat[1, 17],
		'GRM':secMat[2, 17],
		'CCC':secMat[3, 17],
		'HRS':secMat[4, 17],
		'IVS':secMat[5, 17],
		'SEF':secMat[6, 17],
		'DSI':secMat[7, 17],
		'TVM':secMat[8, 17],
		'BCR':secMat[9, 17],
		'STA':secMat[10, 17],
		'IPY':secMat[11, 17],
		'DCS':secMat[12, 17],
		'EKM':secMat[13, 17],
		'MOS':secMat[14, 17],
		'AIS':secMat[15, 17],

		'QoS':qosMat[17, 17],
		'throughput':qosMat[14, 17],
		'performance':qosMat[15, 17],
		'availability':qosMat[16, 17],
		'VMtype':qosMat[3, 14],
		'VMsize':qosMat[4, 14],
		'netBandwidth':qosMat[5, 14],
		'multiTen':qosMat[6, 14],
		'globLat':qosMat[7, 15],
		'totRuntime':qosMat[8, 15],
		'responseTime':qosMat[9, 15],
		'CPUusage':qosMat[10, 15],
		'uptime':qosMat[11, 16],
		'location':qosMat[12, 16],
		'numOutages':qosMat[13, 16],
		'uplink':qosMat[0, 9],
		'downlink':qosMat[1, 9],
		'latency':qosMat[2, 9],
	}

	return chartInfo

# this runs our bayes net
# need to add in more params for user input
# as well as database id's
def runbayesnet(request):
	def f_status(status):
		uptimePercent = 0.7
		if status == 'up':
			return uptimePercent
		elif status == 'down':
			return 1-uptimePercent

	def f_numOutages(numOutages):
		outs = 1
		if numOutages == 'none':
			if outs == 0:
				return 1
			else:
				return 0	
		elif numOutages == 'some':
			if outs >= 0:
				return 1
			else:
				return 0	

	def f_availability(status, numOutages, availability):
		table = dict()
		table['tnt'] = 1
		table['tnf'] = 0
		table['tst'] = 0.8
		table['tsf'] = 0.2
		table['fnt'] = 0.2
		table['fnf'] = 0.8
		table['fst'] = 0.0
		table['fsf'] = 1
		key = ''
		key = key + 't' if status == 'up' else key + 'f'
		key = key + 'n' if numOutages == 'none' else key + 's'
		key = key + 't' if availability else key + 'f'
		return table[key]

	g = build_bbn(
		f_status,
		f_numOutages,
		f_availability,
		domains=dict(
			status=['down', 'up'],
			numOutages=['none', 'some']
			)
		)

	g.q()

	return render(request, 'index.html')

# Not the implementation of the bayes net officially
def montyhall(request):
	# This is just an example to refer to as we implement the 
	# Main bayes net

	def f_prize_door(prize_door):
		return 0.33333333

	def f_guest_door(guest_door):
		return 0.33333333

	def f_monty_door(prize_door, guest_door, monty_door):
		if prize_door == guest_door:  # Guest was correct!
			if prize_door == monty_door:
				return 0	 # Monty never reveals the prize
			else:
				return 0.5   # Monty can choose either goat door
		elif prize_door == monty_door:
			return 0		 # Again, Monty wont reveal the prize
		elif guest_door == monty_door:
			return 0		 # Monty will never choose the guest door
		else:
			# This covers all case where
			# the guest has *not* guessed
			# correctly and Monty chooses
			# the only remaining door that
			# wont reveal the prize.
			return 1

	g = build_bbn(
		f_prize_door,
		f_guest_door,
		f_monty_door,
		domains=dict(
			prize_door=['A', 'B', 'C'],
			guest_door=['A', 'B', 'C'],
			monty_door=['A', 'B', 'C']))

	g.q()

	return render(request, 'index.html')

# This is what is used to call the spider for review collection
# Additionally, this will run the opinion miner on the reviews and update
# the CSP database with the new information
def aggReviews(request):
	# ------------------------------------------- #
	# Aggregate any new reviews into the database #
	# ------------------------------------------- #

	# TODO: Download package to fix ReactorNotRestartable error
	#       and implement it here.

	configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
	runner = CrawlerRunner()

	d = runner.crawl(ReviewSpider)
	#d.addBoth(lambda _: reactor.stop())
	#reactor.run() # the script will block here until the crawling is finished

	# update averages for the CSP scores #
	# updateAverages()

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
