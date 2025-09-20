from django.db import models
from django.contrib.auth.models import AbstractUser
from businesses.models import Business

class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True)
    first_seen_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict, blank=True)

    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("user", "User"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    USERNAME_FIELD = "username"   # You can also use "phone"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username or self.phone
