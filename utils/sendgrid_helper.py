import os
from postmarker.core import PostmarkClient

# Postmark
POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY')
FROM_EMAIL = os.environ.get('POSTMARK_FROM_EMAIL')  # misal: "no-reply@hubsensi.com"
TEMPLATE_ID = int(os.environ.get('POSTMARK_TEMPLATE_ID', 0))  # template Hubsensi Login Info
LOGO_URL = os.environ.get('LOGO_URL')  # URL statis logo

if not POSTMARK_API_KEY or not FROM_EMAIL or TEMPLATE_ID == 0 or not LOGO_URL:
    raise ValueError("Environment variable Postmark atau LOGO_URL belum lengkap")

postmark_client = PostmarkClient(server_token=POSTMARK_API_KEY)


def send_login_email(to_email: str, name: str, username: str, password: str, login_link: str) -> dict:
    """
    Mengirim email login info menggunakan template Postmark dengan logo statis
    """
    try:
        template_model = {
            "name": name,
            "username": username,
            "password": password,
            "login_link": login_link,
            "logo_url": LOGO_URL
        }

        resp = postmark_client.emails.send_with_template(
            From=FROM_EMAIL,
            To=to_email,
            TemplateId=TEMPLATE_ID,
            TemplateModel=template_model
        )

        return {
            "status_code": 200 if resp.get('ErrorCode') == 0 else resp.get('ErrorCode'),
            "body": resp,
            "headers": {}
        }

    except Exception as e:
        raise RuntimeError(f"Gagal mengirim email login info: {e}")
