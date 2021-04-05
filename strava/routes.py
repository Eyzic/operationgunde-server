from flask import Flask, Blueprint, render_template, session, redirect, jsonify, request
from strava.models import *
import json
import config
from stravaio import StravaIO
from stravaio import strava_oauth2
import requests
import urllib3
import os.path
import glob

strava_page = Blueprint('strava_page', __name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@strava_page.route("/strava/authorize", methods=['GET'])
def authorize():
    oauth2 = strava_oauth2(client_id=config.strava['client_id'], client_secret=config.strava['client_secret'])
    access_token = oauth2['access_token']

    load_athlete(access_token)
    load_activities(access_token)
    
    return jsonify('OK')

# Send a parameter in JSON of the ID and get name as a return
# Retrieves from local storage
@strava_page.route('/strava/athlete', methods=['GET'])
def athlete():
    id = request.args.get('id')
    dir_name = os.path.join(os.path.expanduser('~'), '.stravadata')
    f_name = os.path.join(dir_name, f"athlete_{id}.json")
    try:
        with open(f_name, 'r') as f:
            data = json.load(f)
            rv = {'firstname': data['firstname'],
                  'lastname': data['lastname'],
                  'id': id}
    except Exception as error:
        print(error)
        rv = None

    return rv

# Returns all activity data from athlete ID
# Params = {'id'}
# Retrieves from local storage
@strava_page.route("/strava/activities")
def activities():

    athlete_id = request.args.get('id')
    dir_activities = os.path.join(os.path.expanduser('~'), f'.stravadata/activities_{athlete_id}')

    if not os.path.exists(dir_activities):
        return "Directory missing"

    list = []

    for file_name in glob.glob(os.path.join(dir_activities, '*.json')):
        with open(file_name) as f:
            data = json.load(f)
            
            json_activity = {
                'id': data['id'],
                'athlete': data['athlete'],
                'start_date': data['start_date'],
                'start_date_local': data['start_date_local'],
                'distance': data['distance'],
                'moving_time': data['moving_time'],
                'elapsed_time': data['elapsed_time'],
                'type': data['type']
            }

            list.append(json_activity)

    return jsonify(list)

# Return all stored athletes in local storage
@strava_page.route("/strava/athlete_all")
def athlete_all():

    dir_name = os.path.join(os.path.expanduser('~'), '.stravadata')
    list = []

    for file_name in glob.glob(os.path.join(dir_name, '*.json')):
        with open(file_name) as f:
            data = json.load(f)
            
            json_athlete = {
                'firstname': data['firstname'],
                'lastname': data['lastname'],
                'id': data['id']
            }

            list.append(json_athlete)

    return jsonify(list)

# Load athlete into local storage
def load_athlete(access_token):
    client = StravaIO(access_token)
    athlete = client.get_logged_in_athlete()
    athlete_id = athlete.api_response.id
    f_name = os.path.join(os.path.expanduser('~'), f'.stravadata/athlete_{athlete_id}.json')
    
    if os.path.isfile(f_name):
        print("Already stored")
    else:
        athlete.store_locally()
        print(f"Athlete {athlete.to_dict()['id']} stored")

# Load athletes acitivties into local storage
def load_activities(access_token):
    client = StravaIO(access_token)
    activities = client.get_logged_in_athlete_activities(after='2021-04-01')
    athlete_id = client.get_logged_in_athlete().api_response.id

    for a in activities:
        activity_id = a.id
        activity = client.get_activity_by_id(activity_id)
        f_name = os.path.join(os.path.expanduser('~'), f'.stravadata/activities_{athlete_id}/activity_{activity_id}.json')

        if os.path.isfile(f_name):
            print("Already stored")
        else:
            activity.store_locally()
            print(f"Activity {activity.to_dict()['id']} stored")

#def store_mongo():
