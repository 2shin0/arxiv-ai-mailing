import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT = os.getenv("RECIPIENT")

# Google Sheets 설정
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
GOOGLE_WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME")
GOOGLE_API_CREDENTIALS_PATH = os.getenv("GOOGLE_API_CREDENTIALS_PATH")
GOOGLE_SCRIPT_ID = os.getenv("GOOGLE_SCRIPT_ID")