# celery_init.py
from factory import create_app
from celery_worker import celery

# Buat instance aplikasi Flask hanya untuk memberikan konteks ke Celery
flask_app = create_app()

# Dorong konteks aplikasi agar tersedia untuk worker
flask_app.app_context().push()