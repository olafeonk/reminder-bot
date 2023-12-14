import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_URL = os.getenv("API_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
IAM_TOKEN = os.getenv("IAM_TOKEN")
