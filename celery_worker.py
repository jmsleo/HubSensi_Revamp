# HubSensi_(GitHub Production)/celery_worker.py
import os
from celery import Celery
from dotenv import load_dotenv

# Muat environment variables terlebih dahulu
load_dotenv()

# Buat instance Celery dan beritahu di mana letak file tasks.py
celery = Celery(
    "HubSensi",
    broker=os.environ.get('CELERY_BROKER_URL'),
    backend=os.environ.get('CELERY_RESULT_BACKEND'),
    include=['tasks']  # <-- Baris ini adalah kuncinya
)

# Konfigurasi tambahan (opsional tapi bagus untuk dimiliki)
celery.conf.update(
    task_track_started=True,
)