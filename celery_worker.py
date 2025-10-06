# celery_worker.py
import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    __name__,
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
)

def init_celery(app):
    """Integrasikan Celery dengan konteks Flask"""
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask
    return celery
