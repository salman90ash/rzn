from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from .jobs import my_job, my_updates


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_updates, 'cron', hour='8-23', minute='*/15')
    scheduler.start()
