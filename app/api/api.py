import urllib.parse

import requests

import datetime

import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

API_URL = os.getenv("API_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
IAM_TOKEN = os.getenv("IAM_TOKEN")


def create_task(telegram_id, message, time: datetime.datetime):
    headers = {"Authorization": f"Bearer {IAM_TOKEN}"}
    start_time = time.strftime("%Y-%m-%d %H:%M:%S").encode("UTF-8")
    body = {"telegram_id": telegram_id, "text": message, "start_time": start_time}
    requests.post(f"{API_URL}/api/tasks", headers=headers, data=body)


def list_tasks(telegram_id):
    headers = {"Authorization": f"Bearer {IAM_TOKEN}"}
    r = requests.get(f"{API_URL}/api/telegram/{telegram_id}", headers=headers)
    d = r.json()
    message = []
    for elem in d["data"]:
        text = urllib.parse.unquote(elem["text"])
        date: datetime = datetime.datetime.strptime(elem["start_time_at"], "%Y-%m-%dT%H:%M:%SZ")
        message.append((text, date))
    return message


