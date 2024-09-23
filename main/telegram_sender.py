import os

import requests

TOKEN = os.getenv("API_TOKEN_BOT")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message(chat_id, message):

    params = {"chat_id": chat_id, "text": message}
    try:
        requests.get(URL, params)
    except requests.exceptionsConnectionError as e:
        print(f"Error sending message: {e}")
