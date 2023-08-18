from django.db import models
from django.apps import apps

class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    facility = models.ForeignKey('map.Facility', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_facility(self):
        Facility = apps.get_model('map', 'Facility')
        return Facility.objects.get(pk=self.facility_id)