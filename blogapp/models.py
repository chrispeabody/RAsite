from django.db import models

# Create your models here.

class Test(models.Model):
    name = models.CharField(max_length=30)
    
    description = models.CharField(max_length=4000)

class Note(models.Model):
    title = models.CharField(max_length=30)

    userid = models.IntegerField()
    
    description = models.CharField(max_length=4000)

