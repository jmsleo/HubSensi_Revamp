# celery_init.py
import logging
from factory import create_app
from celery_worker import celery

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Buat instance aplikasi Flask hanya untuk memberikan konteks ke Celery
    logger.info("Creating Flask app for Celery context...")
    flask_app = create_app()

    # Dorong konteks aplikasi agar tersedia untuk worker
    flask_app.app_context().push()
    logger.info("Flask app context pushed successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize Celery with Flask context: {e}")
    raise