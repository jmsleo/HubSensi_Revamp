web: flask db upgrade && gunicorn main:app --bind 0.0.0.0:$PORT
worker: celery -A celery_worker.celery worker --loglevel=info