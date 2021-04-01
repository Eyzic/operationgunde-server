import requests
import datetime
from bson.json_util import loads, dumps
import json


BASE = "http://127.0.0.1:5000/"

payload = {
        'user': 2,
        'date': str(datetime.date.today())
    }

response = requests.get(BASE + "api/stats", params=payload)
print(response.json())

payload = {
        'user': 2,
        # 'date': str(datetime.date.today())
        'date': '2020-03-29'
    }

response = requests.delete(BASE + "api/stats", params=payload)
print(response.json())

payload = {
        'user': 2,
        'date': str(datetime.date.today()),
        'hrv': 64,
        'sleeping_hours': 7,
        'stress_level': 6,
        'muscle_ache': 3,
        'mood_level': 8,
        'injury_level' : 10,
        'energy_level': 5
    }

response = requests.post(BASE + "api/stats", params=payload)
print(response.json(), '\n')

payload = {
        'user': 2,
        'date': str(datetime.date.today())
    }

response = requests.get(BASE + "api/stats/hrv", params=payload)
print(response.json())