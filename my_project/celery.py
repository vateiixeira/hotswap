from __future__ import absolute_import
from datetime import timedelta
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
app = Celery('my_project')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

app.conf.update(
    enable_utc=True,
    #broker_url=config('CELERY_BROKER_URL', 'redis://{}:{}/0'.format(settings.REDIS_HOST, settings.REDIS_PORT)),
    # broker_transport_options={
    #     'visibility_timeout': 3600,
    #     'fanout_prefix': True,
    #     'fanout_patterns': True,
    # },
    #result_backend=config('CELERY_RESULT_BACKEND', 'redis://{}:{}/0'.format(settings.REDIS_HOST, settings.REDIS_PORT)),
    timezone='America/Sao_Paulo',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    #task_default_queue=task_default_queue,
    # task_queues=(
    #     Queue(task_default_queue, Exchange(), routing_key=task_default_queue),
    # ),
    beat_schedule={ 
        #colocar tasks beat aqui   
        'core.envia_email_notas_presas':{
            'task': 'my_project.core.tasks.envia_email_notas_presas',
            'schedule': timedelta(minutes=3)
        },    
        'core.notas_socin':{
            'task': 'my_project.core.tasks.notas_socin',
            'schedule': timedelta(minutes=3)
        },    
    }
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
