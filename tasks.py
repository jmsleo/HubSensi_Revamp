from celery_worker import celery
from utils.sendgrid_helper import send_login_email
from flask import url_for

@celery.task
def send_email_task(to_email: str, name: str, username: str, password: str):
    """
    Task untuk mengirim email informasi login di background.
    """
    try:
        login_link = url_for('auth.login', _external=True)
        send_login_email(
            to_email=to_email,
            name=name,
            username=username,
            password=password,
            login_link=login_link
        )
        return f"Email berhasil dikirim ke {to_email}"
    except Exception as e:
        print(f"Gagal mengirim email ke {to_email}: {e}")
        return f"Gagal mengirim email: {e}"