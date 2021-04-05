import config as config 
from stravaio import StravaIO
from stravaio import strava_oauth2
from database import *
import numpy
import requests
import urllib3
import os.path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def init_strava():
    # Strava API database
    oauth2 = strava_oauth2(client_id=config.strava['client_id'], client_secret=config.strava['client_secret'])
    config.strava['access_token'] = oauth2['access_token']
    

def refresh_token():
    
    auth_url = "https://www.strava.com/oauth/token"

    payload = {
        'client_id': config.strava['client_id'],
        'client_secret': config.strava['client_secret'],
        'refresh_token': config.strava['refresh_token'],
        'grant_type': 'refresh_token',
        'f': 'json'
    }

    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']

    return access_token



