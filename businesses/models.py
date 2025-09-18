from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=200)
    google_location_id = models.CharField(max_length=200, blank=True, null=True)
    google_api_creds = models.JSONField(null=True, blank=True)
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
