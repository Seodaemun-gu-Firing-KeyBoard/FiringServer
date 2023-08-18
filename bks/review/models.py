from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps

class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    facility = models.ForeignKey('map.Facility', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_facility(self):
        Facility = apps.get_model('map', 'Facility')
        return Facility.objects.get(pk=self.facility_id)