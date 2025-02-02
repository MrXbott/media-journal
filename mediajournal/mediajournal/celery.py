import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediajournal.settings')

app = Celery('mediajournal')
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks()