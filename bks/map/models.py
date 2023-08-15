from django.db import models

# Create your models here.
class Facility(models.Model):
    name = models.TextField(blank=True, null=True)
    target = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    use = models.TextField(blank=True, null=True)
    reception = models.TextField(blank=True, null=True)
    select = models.TextField(blank=True, null=True)
    recruit = models.TextField(blank=True, null=True)
    application = models.TextField(blank=True, null=True)
    cancel = models.TextField(blank=True, null=True)
    fee = models.TextField(blank=True, null=True)
    reserve = models.TextField(blank=True, null=True)
    call = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, null=True)