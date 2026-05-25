import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GreenArchiveBackend.settings')

app = Celery('GreenArchiveBackend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Define the periodic task schedule (Celery Beat)
app.conf.beat_schedule = {
    'run-cleanup-every-3-days': {
        # Point this to the absolute module path of this file
        'task': 'GreenArchiveBackend.celery.my_periodic_task',
        # Corrected: Run every 3 days at midnight (00:00)
        'schedule': crontab(day_of_month='*/3', hour=0, minute=0),
    },
}

# Define your task at the bottom of the initialization file
@app.task
def my_periodic_task():
    # Place your application logic here (e.g., database cleanups, syncing data)
    print("Periodic task executed successfully!")
    return "Done"