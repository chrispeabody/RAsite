from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

# List of each app and their information
###############################################
# DEPRICATED: THIS ENTIRE CLASS IS NEVER USED #
###############################################
class App(models.Model):
	user = models.ForeignKey(
		User, # If we try to exapand user, this could cause issues?
		on_delete=models.CASCADE,
	)

	currCSP = models.CharField(max_length=40) #models.ForeignKey(
	#	'CSP',
	#	on_delete=models.CASCADE,
	#)

	locX = models.FloatField()
	locY = models.FloatField()


# List of all CSP's and their information
class CSP(models.Model):
	name = models.CharField(max_length=40, primary_key= True)
	codename = models.CharField(max_length=40)

	# Opinion information  gathered from review text
	opPositive = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)], null = True)
	opNeutral = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)], null = True)
	opNegative = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)], null = True)

	# Average of all star ratings for this CSP
	avgRating = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)], null = True)

	# ----------------- #
	# Simulation Bounds #
	# ----------------- #

	# Future work: For anything that needs to be randomized, do it once and store it here
	# for each given CSP

	# -------------- #
	# Data Graveyard #
	# -------------- #

	### We may not need the below information, especially if it is collected live ###
	### That way it doesn't need to be stored. For now, we comment it all out ###

	## Percentage of time in the last thirty days that CSP was up
	#UptimePercent = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(100.0)], null = True)
	
	## Number of outages the CSP had in the last 30 days
	#NumOutages = models.IntegerField(validators = [MinValueValidator(1)], null = True)

	## Number of copies of data the CSP keeps
	#redundVal = models.IntegerField(validators = [MinValueValidator(1)], null = True)

	def __str__(self):
		return self.name
		#return self.codename

# List of all the locations for each CSP
###############################################
# DEPRICATED: THIS ENTIRE CLASS IS NEVER USED #
###############################################
class CSPLoc(models.Model):
	CSP = models.CharField(max_length=40) #models.ForeignKey(
	#	'CSP',
	#	on_delete=models.CASCADE
	#)

	locX = models.FloatField()
	locY = models.FloatField()

	def __str__(self):
		return self.name

	# Perhaps modify this to hold private user locations as well

# Category scores, for specific categories
class CatScore(models.Model):
	# What CSP is this score about?
	CSP = models.CharField(max_length=40) #models.ForeignKey(
	#	'CSP',
	#	on_delete=models.CASCADE
	#)

	# What type of score is it
	type = models.CharField(max_length=12)

	# What is the score in terms of percentage
	value = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)])

# Holds the weights for the cloud security control groups
class CtrlGrpWeight(models.Model):
	# Which control group (AIS, AAC, BCR, etc)
	ctrlGroup = models.CharField(max_length=3)

	# Domain (Data, App, Storage, etc)
	domain = models.CharField(max_length=8)

	# the actual weight to store
	weight = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)])

# Holds any numerical type rating for a CSP
class Rating(models.Model):
	# The unique id of the rating. We steal it for use in our database too, so we don't duplicate ratings
	idNum = models.IntegerField(unique=True, null=False)

	# What CSP is this rating about?
	CSP = models.CharField(max_length=40) #models.ForeignKey(
	#	'CSP',
	#	on_delete=models.CASCADE
	#)

	# What type of rating is it?
	type = models.CharField(max_length=12)

	# What's the rating in terms of percentage?
	value = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)])

	# Where did we get the rating?
	source = models.CharField(max_length=100, null = True)

	# When was the rating made?
	dateMade = models.DateField(auto_now=False, auto_now_add=False, null = True)

	# Where was the rating made?
	locMade = models.CharField(max_length=100, null = True)

# Holds any textual feedback for a CSP
class Review(models.Model):
	# The unique id of the review. We steal it for use in our database too, so we don't duplicate reviews
	idNum = models.IntegerField(unique=True, null=True)

	# What CSP is this review about?
	CSP = models.CharField(max_length=40) #models.ForeignKey(
	#	'CSP',
	#	on_delete=models.CASCADE
	#)

	# The review itself
	plaintext = models.CharField(max_length=20000, null = True) # Adjust size?

	# Where did we get the review?
	source = models.CharField(max_length=100, null = True)

	# When was the review made?
	dateMade = models.DateField(auto_now=False, auto_now_add=False, null = True)

	# Where was the review made?
	locMade = models.CharField(max_length=100, null = True)

# Stores already calculated trust scores
class TrustScore(models.Model):
	# What user/app is this score for?
	user = models.ForeignKey(
		User, # If we try to exapand user, this could cause issues?
		on_delete=models.CASCADE,
	)

	# What CSP is this score for?
	CSP = models.CharField(max_length=40) #models.ForeignKey(
	#	'CSP',
	#	on_delete=models.CASCADE
	#)

	# What is the value of the score?
	value = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(100.0)])

	