import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "HubSensi-Celery", # Anda bisa beri nama apa saja
    backend=os.environ.get('CELERY_RESULT_BACKEND'),
    broker=os.environ.get('CELERY_BROKER_URL')
)