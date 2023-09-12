import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab



# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shima.settings')


app = Celery('shima')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule= {
    'create-attantance-avery maoning':{
        'task':'userapp.tasks.asign_attendance',
        'schedule': crontab(hour=11,minute=34),

    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')