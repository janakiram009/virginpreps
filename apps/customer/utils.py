import random
from django.core.cache import cache

def generate_otp(phone):
    otp = str(random.randint(100000, 999999))
    cache.set(f'otp_{phone}', otp, timeout=300)
    return otp

def verify_otp(phone, otp_input):
    otp = cache.get(f'otp_{phone}')
    return otp == otp_input

import requests

def send_sms_via_fast2sms(phone, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "variables_values": otp,
        "route": "otp",
        "numbers": phone
    }
    headers = {
        'authorization': 'YOUR_FAST2SMS_API_KEY',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
