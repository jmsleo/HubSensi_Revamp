web: flask db upgrade && gunicorn app:app --bind 0.0.0.0:$PORT
worker: celery -A celery_worker.celery worker --loglevel=info