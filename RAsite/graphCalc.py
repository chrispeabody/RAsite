# graphCalc.py
# Holds all the functionality for OUR graph

from CSPtool.models import CSP, Review, Rating, CatScore
import numpy
import random
random.seed()

# a utility function for making zeros really close to zero instead
# also makes sure normalizing worked
def unZero(num):
	if num < 0 or num > 1:
		print ("################################################")
		print ("###### \"Normalized\" number was NOT normal ######")
		print ("################################################")
	elif num > 0 and num < 0.01:
		return 0.01
	else:
		return num

# A utility function for probability propogation
#def bayes(priorBelief, *args):
#	numAndDen = priorBelief
#	for arg in args:
#		numAndDen *= (arg / priorBelief)

#	denom2 = 1 - priorBelief
#	for arg in args:
#		denom2 *= (arg / (1-priorBelief))

#	newProb = numAndDen / (numAndDen + denom2)
#	return newProb

# Bad bayesian network calculation
def bayes(priorBelief, *args):
	num = priorBelief
	for arg in args:
		num *= arg

	return num

# Calculates the cost node
def cost():
	# NODE NUMBERS #
	#0 - Data Consumed
	#1 - Transactions Processed
	#2 - API Requests

	#3 - Number of Cores
	#4 - Disk I/O
	#5 - Storage Size

	#6 - OS
	#7 - Bandwidth

	#8 - Usage Based
	#9 - Tiered Based

	#10 - Infrustructure as a service
	#11 - Platform as a service
	#12 - Software as a service

	#13 - Cost

	a = numpy.zeros((14, 14))

	def initMat(mat):
		# NODE NUMBERS #
		#0 - Data Consumed
		mat[0, 8] = (random.randint(50, 1024) - 50) / 974
		mat[0, 8] = unZero(mat[0, 8])

		#1 - Transactions Processed
		mat[1, 8] = random.randint(1, 1000000) / 1000000
		mat[1, 8] = unZero(mat[1, 8])

		#2 - API Requests
		mat[2, 8] = (random.randint(100, 1000) - 100) / 900
		mat[2, 8] = unZero(mat[2, 8])

		#3 - Number of Cores
		mat[3, 10] = (random.randint(1, 128) - 1) / 127
		mat[3, 10] = unZero(mat[3, 10])

		#4 - Disk I/O
		mat[4, 10] = (random.randint(43636, 160000) - 43636) / 116364
		mat[4, 10] = unZero(mat[4, 10])

		#5 - Storage Size
		mat[5, 10] = (random.randint(2, 2048) - 2) / 2046
		mat[5, 10] = unZero(mat[5, 10])

		#6 - OS
		OSnum = random.uniform(0.01, 1)
		mat[6, 10] = OSnum
		mat[6, 11] = OSnum

		#7 - Bandwidth
		mat[7, 11] = (random.randint(100, 2048) - 100) / 1948
		mat[7, 11] = unZero(mat[7, 11])

		#9 - Tiered Based
		mat[9, 12] = (random.uniform(0.05, 0.181) - 0.05) / 0.176
		mat[9, 12] = unZero(mat[9, 12])

		# ------------------- #
		# Prior belief scores #
		# ------------------- #

		#8 - Usage Based
		mat[8, 12] = random.uniform(0.01, 1)

		#10 - Infrustructure as a service
		mat[10, 13] = random.uniform(0.01, 1)

		#11 - Platform as a service
		mat[11, 13] = random.uniform(0.01, 1)

		#12 - Software as a service
		mat[12, 13] = random.uniform(0.01, 1)

		#13 - Cost
		mat[13, 13] = random.uniform(0.01, 1)

	def calcUsageBased(mat):
		mat[8, 12] = bayes(mat[8, 12], mat[0, 8], mat[1, 8], mat[2, 8])

	def calcIaaS(mat):
		mat[10, 13] = bayes(mat[10, 13], mat[3, 10], mat[4, 10], mat[5, 10], mat[6, 10])

	def calcPaaS(mat):
		mat[11, 13] = bayes(mat[11, 13], mat[6, 11], mat[7, 11])

	def calcSaaS(mat):
		mat[12, 13] = bayes(mat[12, 13], mat[8, 12], mat[9, 12])

	def calcCost(mat):
		mat[13, 13] = bayes(mat[13, 13], mat[10, 13], mat[11, 13], mat[12, 13])

	initMat(a)
	calcUsageBased(a)
	calcIaaS(a)
	calcPaaS(a)
	calcSaaS(a)
	calcCost(a)

	return (a[13, 13], a)

# Calculates user quality of experience
def userQoE(cspname):
	# NODE NUMBERS #
	#0 - Support score
	#1 - Computation score
	#2 - Security score
	#3 - Performance score
	#5 -> #4 - Star rating
	#6 -> #5 - Review score
	#7 -> #6 - Reputation

	a = numpy.zeros((7, 7))

	# takes numpy.matrix of 8x8
	def initMat(mat):
		#0 - Support score
		mat[0, 4] = CatScore.objects.get(CSP=cspname, type='support').value
		mat[0, 4] = unZero(mat[0, 4])

		#1 - Computation score
		mat[1, 4] = CatScore.objects.get(CSP=cspname, type='computing').value
		mat[1, 4] = unZero(mat[1, 4])
		
		#2 - Security score
		mat[2, 4] = CatScore.objects.get(CSP=cspname, type='security').value
		mat[2, 4] = unZero(mat[2, 4])

		#3 - Performance score
		mat[3, 4] = CatScore.objects.get(CSP=cspname, type='performance').value
		mat[3, 4] = unZero(mat[3, 4])

		#6 - Review score
		csp = CSP.objects.get(name=cspname)
		revscore = (csp.opPositive - csp.opNegative + 1) / 2
		mat[5, 6] = revscore
		mat[5, 6] = unZero(mat[5, 6])

		# ------------------- #
		# Prior belief scores #
		# ------------------- #

		#4 - Star rating
		mat[4, 6] = CSP.objects.get(name=cspname).avgRating
		mat[4, 6] = unZero(mat[4, 6])

		#6 - Reputation
		mat[6, 6] = random.uniform(0.01, 1)

	def calcStarRating(mat):
		#4 - Category scores
		mat[4, 6] = bayes(mat[4, 6], mat[0, 4], mat[1, 4], mat[2, 4], mat[3, 4])

	def calcRep(mat):
		#7 - Reputation
		mat[6, 6] = bayes(mat[6, 6], mat[4, 6], mat[5, 6])

	initMat(a)
	calcStarRating(a)
	calcRep(a)

	return (a[6, 6], a)

# Calculates the network quality of servive
def networkQoS():
	# NODE NUMBERS #
	#0 - Uplink
	#1 - Downlink
	#2 - Latency

	#3 - VM Type
	#4 - VM Size
	#5 - Network Bandwidth
	#6 - Multitenancy

	#7 - Global Latency
	#8 - Total Runtime
	#9 - Response Time
	#10 - CPU Speed
	
	#11 - Uptime (%)
	#12 - Location
	#13 - Number of Outages

	#14 - Throughput
	#15 - Performance
	#16 - Availability

	#17 - Network QoS

	a = numpy.zeros((18,18))

	def initMat(mat):
		#0 - Uplink
		mat[0, 9] = (random.uniform(1.87, 100.97) - 1.87) / 99.1
		mat[0, 9] = unZero(mat[0, 9])

		#1 - Downlink
		mat[1, 9] = (random.uniform(3.4, 179.22) - 3.4) / 175.82
		mat[1, 9] = unZero(mat[1, 9])

		#2 - Latency
		mat[2, 9] = (random.randint(26, 344) - 26) / 318
		mat[2, 9] = unZero(mat[2, 9])

		#3 - VM Type
		mat[3, 14] = (random.randint(1, 4) - 1) / 3
		mat[3, 14] = unZero(mat[3, 14])

		#4 - VM Size
		mat[4, 14] = random.uniform(0, 1)
		mat[4, 14] = unZero(mat[4, 14])

		#5 - Network Bandwidth
		mat[5, 14] = (random.uniform(1.6, 6.4) - 1.6) / 4.8
		mat[5, 14] = unZero(mat[5, 14])

		#6 - Multitenancy
		mat[6, 14] = (random.randint(1, 10) - 1) / 9
		mat[6, 14] = unZero(mat[6, 14])

		#7 - Global Latency
		mat[7, 15] = (random.randint(15, 188) - 15) / 173
		mat[7, 15] = unZero(mat[7, 15])

		#8 - Total Runtime
		mat[8, 15] = random.randint(0, 1200) / 1200
		mat[8, 15] = unZero(mat[8, 15])

		#10 - CPU Speed
		mat[10, 15] = (random.randint(1000, 20000) - 1000) / 19000
		mat[10, 15] = unZero(mat[10, 15])

		#11 - Uptime (%)
		mat[11, 16] = random.uniform(0, 100) / 100
		mat[11, 16] = unZero(mat[11, 16])

		#12 - Location
		mat[12, 16] = random.uniform(0, 1)
		mat[12, 16] = unZero(mat[12, 16])

		#13 - Number of Outages
		mat[13, 16] = random.uniform(0, 1)
		mat[13, 16] = unZero(mat[13, 16])

		# ------------------- #
		# Prior belief scores #
		# ------------------- #

		#9 - Response time
		mat[9, 15] = random.uniform(0.01, 1)

		#14 - Throughput
		mat[14, 17] = random.uniform(0.01, 1)

		#15 - Performance
		mat[15, 17] = random.uniform(0.01, 1)

		#16 - Availability
		mat[16, 17] = random.uniform(0.01, 1)

		#17 - Network QoS
		mat[17, 17] = random.uniform(0.01, 1)

	def calcResponseTime(mat):
		mat[9, 15] = bayes(mat[9, 15], mat[0, 9], mat[1, 9], mat[2, 9])

	def calcThroughput(mat):
		mat[14, 17] = bayes(mat[14, 17], mat[3, 14], mat[4, 14], mat[5, 14], mat[6, 14])

	def calcPerformance(mat):
		mat[15, 17] = bayes(mat[15, 17], mat[7, 15], mat[8, 15], mat[9, 15], mat[10, 15])

	def calcAvailability(mat):
		mat[16, 17] = bayes(mat[16, 17], mat[11, 16], mat[12, 16], mat[13, 16])

	def calcNetworkQoS(mat):
		mat[17, 17] = bayes(mat[17, 17], mat[14, 17], mat[15, 17], mat[16, 17])

	initMat(a)
	calcResponseTime(a)
	calcThroughput(a)
	calcPerformance(a)
	calcAvailability(a)
	calcNetworkQoS(a)

	return (a[17, 17], a)

# Calculates the security of the cloud
def cloudSecurity():
	# NODE NUMBERS #
	#0 - AAC
	#1 - IAM
	#2 - GRM
	#3 - CCC
	#4 - HRS
	#5 - IVS
	#6 - SEF
	#7 - DSI
	#8 - TVM
	#9 - BCR
	#10 - STA
	#11 - IPY
	#12 - DCS
	#13 - EKM
	#14 - MOS
	#15 - AIS
	#16 - Control group Bias
	
	#17 - Overall STAR Score
	#18 - Control group scores
	#19 - Cloud Security

	a = numpy.zeros((19, 19))

	# a utility function for getting the question amounts
	def yesNoNa(rangeNum):
		yes = random.randint(1, rangeNum)
		rangeNum -= yes

		no = random.randint(0, rangeNum)
		rangeNum -= no

		na = rangeNum

		return (yes, no, na)

	def initMat(mat):
		#0 - AAC
		sz = 12
		ynn = yesNoNa(sz)
		mat[0, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#1 - IAM
		sz = 40
		ynn = yesNoNa(sz)
		mat[1, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#2 - GRM
		sz = 22
		ynn = yesNoNa(sz)
		mat[2, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#3 - CCC
		sz = 10
		ynn = yesNoNa(sz)
		mat[3, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#4 - HRS
		sz = 24
		ynn = yesNoNa(sz)
		mat[4, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#5 - IVS
		sz = 33
		ynn = yesNoNa(sz)
		mat[5, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#6 - SEF
		sz = 13
		ynn = yesNoNa(sz)
		mat[6, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#7 - DSI
		sz = 17
		ynn = yesNoNa(sz)
		mat[7, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#8 - TVM
		sz = 10
		ynn = yesNoNa(sz)
		mat[8, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#9 - BCR
		sz = 22
		ynn = yesNoNa(sz)
		mat[9, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2
		
		#10 - STA
		sz = 20
		ynn = yesNoNa(sz)
		mat[10, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#11 - IPY
		sz = 8
		ynn = yesNoNa(sz)
		mat[11, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2
		
		#12 - DCS
		sz = 11
		ynn = yesNoNa(sz)
		mat[12, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2
		
		#13 - EKM
		sz = 14
		ynn = yesNoNa(sz)
		mat[13, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2
		
		#14 - MOS
		sz = 29
		ynn = yesNoNa(sz)
		mat[14, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		#15 - AIS
		sz = 9
		ynn = yesNoNa(sz)
		mat[15, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2
		
		#16 - Overall STAR Score
		sz = 295
		ynn = yesNoNa(sz)
		mat[16, 18] = ((ynn[0] / sz) - (ynn[1] / sz) + 1) / 2

		# ------------------- #
		# Prior belief scores #
		# ------------------- #

		#17 - Control Group Scores
		mat[17, 18] = random.uniform(0.01, 1)

		#18 - Cloud Security
		mat[18, 18] = random.uniform(0.01, 1)

	# VVV THIS CALCULATION NEEDS TO BE DONE  VVV #
	def calcControlGroupScores(mat):
		#17 - Control group scores
		mat[17, 18] = (mat[0, 18] + mat[1, 18] + mat[2, 18] + mat[3, 18] +
			mat[4, 18] + mat[5, 18] + mat[6, 18] + mat[7, 18] +
			mat[8, 18] + mat[9, 18] + mat[10, 18] + mat[11, 18] +
			mat[12, 18] + mat[13, 18] + mat[14, 18] + mat[15, 18]) / 16 # average for now

	def calcCloudSecurity(mat):
		mat[18, 18] = bayes(mat[18, 18], mat[16, 18], mat[17, 18])

	initMat(a)
	calcControlGroupScores(a)
	calcCloudSecurity(a)

	return (a[18, 18], a)