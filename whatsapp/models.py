from django.db import models

class WhatsAppLog(models.Model):
    phone = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20)  # sent / failed
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.status}"
