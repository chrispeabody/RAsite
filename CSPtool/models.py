from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

# List of each app and their information
class App(models.Model):
	user = models.ForeignKey(
		User, # If we try to exapand user, this could cause issues?
		on_delete=models.CASCADE,
	)

	currCSP = models.ForeignKey(
		'CSP',
		on_delete=models.CASCADE,
	)

	locX = models.FloatField()
	locY = models.FloatField()

	# ADD OTHER DIAGNOSTIC INFO #

# List of all CSP's and their information
class CSP(models.Model):
	name = models.CharField(max_length=40, primary_key = True)

	fDowntime = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(100.0)])
	uDowntime = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(100.0)])

	redundVal = models.IntegerField(validators = [MinValueValidator(1)])

	# ADD #
	# Privacy policy info
	# Aggregated ratings, if necessary
	# Any other diagnostics

# List of all the locations for each CSP
class CSPLoc(models.Model):
	CSP = models.ForeignKey(
		'CSP',
		on_delete=models.CASCADE
	)

	locX = models.FloatField()
	locY = models.FloatField()

	# Perhaps modify this to hold private user locations as well

# Holds any numerical type rating for a CSP
class Rating(models.Model):
	# What CSP is this rating about?
	CSP = models.ForeignKey(
		'CSP',
		on_delete=models.CASCADE
	)

	# What type of rating is it?
	type = models.CharField(max_length=12)

	# What's the rating in terms of percentage?
	value = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(100.0)])

	# Where did we get the rating?
	source = models.CharField(max_length=100)

	# When was the rating made?
	dateMade = models.DateField(auto_now=False, auto_now_add=False, null = True)

# Holds any textual feedback for a CSP
class Review(models.Model):
	# What CSP is this review about?
	CSP = models.ForeignKey(
		'CSP',
		on_delete=models.CASCADE
	)

	# The review itself
	plaintext = models.CharField(max_length=2000) # Adjust size?

	# When was the review made?
	dateMade = models.DateField(auto_now=False, auto_now_add=False, null = True)

# Stores already calculated trust scores
class TrustScore(models.Model):
	# What user/app is this score for?
	user = models.ForeignKey(
		User, # If we try to exapand user, this could cause issues?
		on_delete=models.CASCADE,
	)

	# What CSP is this score for?
	CSP = models.ForeignKey(
		'CSP',
		on_delete=models.CASCADE
	)

	# What is the value of the score?
	value = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(100.0)])

	