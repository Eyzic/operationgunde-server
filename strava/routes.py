import config as config 
from stravaio import StravaIO
from flask import Flask, Blueprint, render_template, session, redirect, jsonify, request
from database import *
import requests
import urllib3
import swagger_client

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

strava_page = Blueprint('strava_page', __name__)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': config.strava['client_id'],
    'client_secret': config.strava['client_secret'],
    'refresh_token': config.strava['refresh_token'],
    'grant_type': 'refresh_token',
    'f': 'json'
}

res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("\nStrava Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

print(my_dataset)

client = StravaIO(access_token)
client.__dict__
for m in dir(client):
    if not m.startswith('_'):
        print(m)

athlete = client.get_logged_in_athlete()

print(f"""
Name: {athlete.api_response.firstname}, 
Last Name: {athlete.api_response.lastname}
""")

activities = client.get_logged_in_athlete_activities(after='2021-03-10')
print(activities)