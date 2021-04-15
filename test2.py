import requests
import datetime
from bson.json_util import loads, dumps
import json
import time
import os.path
import pathlib
from strava.models import *

BASE = "http://127.0.0.1:5000/"

payload = {
        'id': 74474598
    }

response = requests.get(BASE + "strava/authorize", params=payload)
#response1 = requests.get(BASE + "strava/activities", params=payload)
#response2 = requests.get(BASE + "strava/athlete_all", params=payload)
#response3 = requests.get(BASE + "strava/athlete_all2", params=payload)

print(response.json())
#print(response1.json())
#print(response2.json())
#print(response3.json())
