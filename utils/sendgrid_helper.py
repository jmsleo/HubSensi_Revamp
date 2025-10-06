import os
import logging
from postmarker.core import PostmarkClient

# Setup logging
logger = logging.getLogger(__name__)

# Postmark configuration dengan validation yang lebih baik
POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY')
FROM_EMAIL = os.environ.get('POSTMARK_FROM_EMAIL')
TEMPLATE_ID = os.environ.get('POSTMARK_TEMPLATE_ID', '0')
LOGO_URL = os.environ.get('LOGO_URL')

# Validation dengan error handling yang lebih baik
missing_vars = []
if not POSTMARK_API_KEY:
    missing_vars.append('POSTMARK_API_KEY')
if not FROM_EMAIL:
    missing_vars.append('POSTMARK_FROM_EMAIL')
if not TEMPLATE_ID or TEMPLATE_ID == '0':
    missing_vars.append('POSTMARK_TEMPLATE_ID')
if not LOGO_URL:
    missing_vars.append('LOGO_URL')

if missing_vars:
    error_msg = f"Missing environment variables: {', '.join(missing_vars)}"
    logger.error(error_msg)
    raise ValueError(error_msg)

# Convert TEMPLATE_ID to int dengan error handling
try:
    TEMPLATE_ID = int(TEMPLATE_ID)
except ValueError:
    raise ValueError(f"POSTMARK_TEMPLATE_ID must be a valid integer, got: {TEMPLATE_ID}")

# Initialize Postmark client dengan error handling
try:
    postmark_client = PostmarkClient(server_token=POSTMARK_API_KEY)
except Exception as e:
    logger.error(f"Failed to initialize Postmark client: {e}")
    raise RuntimeError(f"Failed to initialize Postmark client: {e}")


def send_login_email(to_email: str, name: str, username: str, password: str, login_link: str) -> dict:
    """
    Mengirim email login info menggunakan template Postmark dengan logo statis
    Dengan improved error handling dan logging
    """
    try:
        logger.info(f"Preparing to send email to {to_email}")
        
        # Validate input parameters
        if not all([to_email, name, username, password, login_link]):
            raise ValueError("All parameters (to_email, name, username, password, login_link) are required")
        
        template_model = {
            "name": name,
            "username": username,
            "password": password,
            "login_link": login_link,
            "logo_url": LOGO_URL
        }

        logger.debug(f"Sending email with template ID {TEMPLATE_ID} to {to_email}")
        
        resp = postmark_client.emails.send_with_template(
            From=FROM_EMAIL,
            To=to_email,
            TemplateId=TEMPLATE_ID,
            TemplateModel=template_model
        )

        logger.info(f"Postmark response: {resp}")
        
        # Check if response indicates success
        error_code = resp.get('ErrorCode', 0)
        if error_code != 0:
            error_msg = resp.get('Message', 'Unknown error from Postmark')
            logger.error(f"Postmark returned error code {error_code}: {error_msg}")
            raise RuntimeError(f"Postmark error {error_code}: {error_msg}")

        return {
            "status_code": 200,
            "body": resp,
            "headers": {}
        }

    except Exception as e:
        error_msg = f"Gagal mengirim email login info ke {to_email}: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)