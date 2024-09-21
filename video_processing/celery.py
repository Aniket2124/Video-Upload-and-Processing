from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_processing.settings')

app = Celery('video_processing')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')

# Ensure that tasks from all apps are discovered
app.autodiscover_tasks()

# Add the broker connection retry on startup for Celery 6.0+
app.conf.update(
    broker_connection_retry_on_startup=True,
)
