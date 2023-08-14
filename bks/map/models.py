from django.db import models

# Create your models here.
class Facility(models.Model):
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)