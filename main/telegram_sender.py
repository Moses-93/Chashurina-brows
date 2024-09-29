import os

import requests

TOKEN = os.getenv("API_TOKEN_BOT")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message(chat_id, message):
    """
    Відправляє повідомлення в заданий чат через Telegram Bot API.

    Параметри:
    chat_id (int): Унікальний ідентифікатор цільового чату або користувача.
    message (str): Текст повідомлення, яке буде надіслано.

    Повертає:
    None. Якщо повідомлення надіслано успішно, не повертається жодне значення.
    Якщо виникає помилка з'єднання, виводиться повідомлення про помилку у консоль.
    """
    params = {"chat_id": chat_id, "text": message}
    try:
        requests.get(URL, params)
    except requests.exceptions.ConnectionError as e:
        print(f"Помилка при відправленні повідомлення: {e}")
