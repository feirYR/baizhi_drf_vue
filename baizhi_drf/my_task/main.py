import os

import django
from celery import Celery

# app = Celery('baizhi',backend='redis://192.168.42.133:7000/3',broker='redis://192.168.42.133:7000/4')
app = Celery('baizhi')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baizhi_drf.settings.develop")
django.setup()

app.config_from_object('my_task.config')

app.autodiscover_tasks(['my_task.review'])

