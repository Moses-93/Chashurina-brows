from .models import Notes
import requests

TOKEN = '7238231911:AAFtun0SnxGsJbe5zshhQ2ZyOeUqRwQAOuU'
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

def send_message(chat_id, message):
    
    params = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.get(URL, params)
    except requests.exceptionsConnectionError as e:
        print(f'Error sending message: {e}')

