# app/celery_worker.py

import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

def make_celery():
    celery = Celery(
        "webapp",
        broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
        backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
    )
    celery.conf.update(
        timezone='UTC',
        enable_utc=True,
    )
    return celery

celery = make_celery()
