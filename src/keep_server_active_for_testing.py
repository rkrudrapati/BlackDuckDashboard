import requests
import json
from datetime import datetime
from time import sleep


def login():
    url = "http://cdswaggy-auth-v2-server.cloud.pcftest.com/logins"
    payload = json.dumps({
      "applicationId": "Sapphire",
      "username": "esmith",
      "password": "Lion@123"
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    lv_authToken = response.json()["token"]
    return lv_authToken


def get_patient_task_notes(lv_authToken=""):
    url = "https://cdswaggy-patientgateway-v1-server.cloud.pcftest.com/notes/task/236de902-701c-45fc-a15d-aef2876346c1"
    headers = {
        'auth_token': json.dumps(lv_authToken),
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)


while True:
    if datetime.now().minute not in {0, 15, 30, 45}:
        authToken = login()
        get_patient_task_notes(authToken)
        sleep(60)
    else:
        sleep(60)


