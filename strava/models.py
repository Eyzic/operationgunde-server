import config as config 
from stravaio import StravaIO
from stravaio import strava_oauth2
from database import *
import numpy
import requests
import urllib3
import os.path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize Strava API using StravaIO
def init_strava():
    oauth2 = strava_oauth2(client_id=config.strava['STRAVA_CLIENT_ID'], client_secret=config.strava['STRAVA_CLIENT_SECRET'])
    config.strava['STRAVA_ACCESS_TOKEN'] = oauth2['access_token']
    
# Refresh API connectio and get a new access_token
def refresh_token():
    
    auth_url = "https://www.strava.com/oauth/token"

    payload = {
        'client_id': config.strava['STRAVA_CLIENT_ID'],
        'client_secret': config.strava['STRAVA_CLIENT_SECTET'],
        'refresh_token': config.strava['STRAVA_REFRESH_TOKEN'],
        'grant_type': 'refresh_token',
        'f': 'json'
    }

    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']

    return access_token



