from django.db import models

# Create your models here.
class Facility(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    use = models.CharField(max_length=255)
    reception = models.CharField(max_length=255)
    select = models.CharField(max_length=255)
    recruit = models.CharField(max_length=255)
    application = models.CharField(max_length=255)
    fee = models.CharField(max_length=255)
    reserve = models.CharField(max_length=255)
    call = models.CharField(max_length=255)
    image = models.URLField()
