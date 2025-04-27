# app/beat_scheduler.py

from celery.schedules import crontab
from app.celery_worker import celery
from app.tasks import check_and_retrain_model

celery.conf.beat_schedule = {
    "check-and-retrain-every-10-minutes": {
        "task": "app.tasks.check_and_retrain_model",
        "schedule": crontab(minute="*/10"),  # toutes les 10 minutes
    }
}

celery.conf.timezone = "UTC"
