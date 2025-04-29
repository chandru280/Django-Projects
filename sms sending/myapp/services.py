# services.py
import requests
from django.conf import settings

def send_whatsapp_message(phone_number, message):
    url = f"{settings.WASSENGER_BASE_URL}/messages"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.WASSENGER_API_KEY}'
    }
    payload = {
        'phone': phone_number,
        'message': message
    }

    response = requests.post(url, json=payload, headers=headers)
    
    # Handle the response
    if response.status_code == 201:
        return response.json()  # Success
    else:
        return response.status_code, response.text  # Handle errors
