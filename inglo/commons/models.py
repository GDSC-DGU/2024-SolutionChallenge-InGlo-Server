from django.db import models

class SDGs(models.Model):
    name = models.CharField(max_length=100)

class Country(models.Model):
    name = models.CharField(max_length=100)

