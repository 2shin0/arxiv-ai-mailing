import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_ADDRESS = os.getenv("sender_email")
EMAIL_PASSWORD = os.getenv("password")
RECIPIENT = os.getenv("recipient")
# SMTP_SERVER = os.getenv("smtp_server")
# SMTP_PORT = os.getenv("smtp_port")