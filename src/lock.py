import os
import json
import requests
from dotenv import load_dotenv

import utils

base_url = 'https://api.switch-bot.com'
load_dotenv()
# tokenとsecretを貼り付ける
token = os.getenv("TOKEN") # copy and paste from the SwitchBot app V6.14 or later
secret = os.getenv("secret") # copy and paste from the SwitchBot app V6.14 or later
headers = utils.make_request_header(token,secret)

def read_lock_from_json(deviceListJson = '../deviceList.json') -> dict:
    lock = {}
    f = open(deviceListJson,"r",encoding="utf-8")
    jsonfile = json.load(f)
    devices = jsonfile["body"]["deviceList"]

    for device in devices:
        if device["deviceType"] == "Smart Lock":
            device_lock = device
    return device_lock

def get_lock_status(device_lock:dict):
    devices_url = base_url + "/v1.1/devices/"+device_lock["deviceId"]+"/status"
    try:
        # ロックの状態を取得
        res = requests.get(devices_url, headers=headers)
        res.raise_for_status()
        print(res.text)

    except requests.exceptions.RequestException as e:
        print('response error:',e)

def lock(device_lock:dict):
    devices_url = base_url + "/v1.1/devices/"+device_lock["deviceId"]+"/commands"
    data={
            "commandType": "command",
            "command": "lock",
            "parameter":"default",
        }

    try:
        # ロック
        res = requests.post(devices_url, headers=headers,json=data)
        res.raise_for_status()
        print(res.text)

    except requests.exceptions.RequestException as e:
        print('response error:',e)

def unlock(device_lock:dict):
    devices_url = base_url + "/v1.1/devices/"+device_lock["deviceId"]+"/commands"
    data={
            "commandType": "command",
            "command": "unlock",
            "parameter":"default",
        }

    try:
        # ロック
        res = requests.post(devices_url, headers=headers,json=data)
        res.raise_for_status()
        print(res.text)

    except requests.exceptions.RequestException as e:
        print('response error:',e)

lock(read_lock_from_json())
get_lock_status(read_lock_from_json())