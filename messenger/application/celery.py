import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

app = Celery('application')

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'chats.tasks.update_unique_users',
        'schedule': 30.0,
        'args': ()
    },
}
app.conf.timezone = 'UTC'


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
