import os
import time
import hashlib
import hmac
import base64
import requests
import json
from dotenv import load_dotenv

base_url = 'https://api.switch-bot.com'

def make_sign(token: str,secret: str):
    nonce = ''
    t = int(round(time.time() * 1000))
    string_to_sign = bytes(f'{token}{t}{nonce}', 'utf-8')
    secret = bytes(secret, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign, str(t), nonce

def make_request_header(token: str,secret: str) -> dict:
    sign, t, nonce = make_sign(token, secret)
    headers = {
            "Authorization": token,
            "sign": sign,
            "t": str(t),
            "nonce": nonce
        }
    return headers

def get_device_list(deviceListJson = '../deviceList.json'):
    load_dotenv()

    # tokenとsecretを貼り付ける
    token = os.getenv("TOKEN") # copy and paste from the SwitchBot app V6.14 or later
    secret = os.getenv("secret") # copy and paste from the SwitchBot app V6.14 or later

    devices_url = base_url + "/v1.1/devices"

    headers = make_request_header(token, secret)

    try:
        # APIでデバイスの取得を試みる
        res = requests.get(devices_url, headers=headers)
        res.raise_for_status()

        print(res.text)
        deviceList = json.loads(res.text)
        # 取得データをjsonファイルに書き込み
        with open(deviceListJson, mode='wt', encoding='utf-8') as f:
            json.dump(deviceList, f, ensure_ascii=False, indent=2)

    except requests.exceptions.RequestException as e:
        print('response error:',e)

if __name__ == "__main__":
    get_device_list()