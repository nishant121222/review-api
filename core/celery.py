# core/celery.py
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Load task modules for autodiscovery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps (games, reviews, whatsapp)
app.autodiscover_tasks()

# Optional: Test task
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')