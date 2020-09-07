import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aviatatask.settings')

app = Celery('aviatatask')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'update_routes': {
#         'task': 'routes.tasks.update_routes',
#         'schedule': crontab(minute='*/1'),
#     },
# }