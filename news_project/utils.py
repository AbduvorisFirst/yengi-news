import base64
import binascii
import os
import requests
from django.conf import settings


def generate_key(size=50):
    return binascii.hexlify(os.urandom(size)).decode()

def code_decoder(code, decode=False, l=1):
    if decode:
        for i in range(l):
            code = base64.b64decode(code).decode()
        return code
    else:
        for i in range(l):
            code = base64.b64encode(str(code).encode()).decode()
        return code

def send_otp(otp):
    message = f'sizning otp kodingiz {otp}'
    url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={settings.TG_USER_ID}&text={message}&parse_mode=HTML"
    requests.get(url)

def password_is_valid(password: str):
    if 6 >= len(password):
        return 'error1'
    elif len(password) >= 15:
        return 'error1-1'
    kerak = {
        'son': 0,
        'harf': 0,
        'sym': 0,
        'up': 0,
    }
    for i in password:
        if i.isdigit():
            kerak['son'] += 1
        elif i.isupper():
            kerak['up'] += 1
        elif i.isalpha():
            kerak['harf'] += 1
        elif not i.isalnum():
            kerak['sym'] += 1
    if 0 in [kerak['son'], kerak['harf'], kerak['sym'], kerak['up']]:
        errors = {
            kerak['son']: 'error2-1',
            kerak['harf']: 'error2-2',
            kerak['sym']: 'error2-3',
            kerak['up']: 'error2-4',
        }
        return errors.get(0, 'error2')
    return True

def errors():
    return {
        'error1': 'parol juda qisqa',
        'error1-1': 'parol juda uzun',
        'error2': 'parolda kichik va katta harf symbol, son, qatnashsin',
        'error2-1': 'parolda eng kamida 1ta son qatnashsin',
        'error2-2': 'parolda eng kamida 1ta harf qatnashsin',
        'error2-3': 'parolda eng kamida 1ta symbol qatnashsin',
        'error2-4': 'parolda eng kamida 1ta katta harf qatnashsin'

    }







