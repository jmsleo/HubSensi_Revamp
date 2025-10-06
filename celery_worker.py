# HubSensi_(GitHub Production)/celery_worker.py
import os
import logging
from celery import Celery
from dotenv import load_dotenv

# Setup logging untuk Celery
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Muat environment variables terlebih dahulu
load_dotenv()

# Validate Celery configuration
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

if not CELERY_BROKER_URL:
    raise ValueError("CELERY_BROKER_URL environment variable is required")
if not CELERY_RESULT_BACKEND:
    raise ValueError("CELERY_RESULT_BACKEND environment variable is required")

logger.info(f"Initializing Celery with broker: {CELERY_BROKER_URL}")

# Buat instance Celery dan beritahu di mana letak file tasks.py
celery = Celery(
    "HubSensi",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['tasks']  # <-- Baris ini adalah kuncinya
)

# Konfigurasi tambahan untuk production
celery.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Jakarta',
    enable_utc=True,
    # Retry configuration
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    # Error handling
    task_reject_on_worker_lost=True,
    # Logging
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s',
)

logger.info("Celery worker configuration completed")