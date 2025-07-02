import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT = os.getenv("RECIPIENT")
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL")