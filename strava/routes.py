from flask import Flask, Blueprint, render_template, session, redirect, jsonify, request, url_for
from strava.models import *
import json
import config
from stravaio import StravaIO
from stravaio import strava_oauth2
from database import db
import requests
import urllib3
import urllib
import os.path
import glob
import webbrowser

strava_page = Blueprint('strava_page.authorization_successful', __name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Generate authorization URL to authorization the Strava API
@strava_page.route("/strava/authorize")
def authorize():
    
    app_url = 'http://127.0.0.1:5000'
    params = {
        "client_id": config.strava['STRAVA_CLIENT_ID'],
        "response_type": "code",
        "redirect_uri": f"{app_url}/strava/authorization_successful",
        "scope": "read,profile:read_all,activity:read",
        "state": 'mystate',
        "approval_prompt": "force"
    }
    values_url = urllib.parse.urlencode(params)
    base_url = 'https://www.strava.com/oauth/authorize'
    rv = base_url + '?' + values_url
    # print(f"Authorize url = {rv}")
    
    webbrowser.get().open(rv)

    return jsonify(rv)

# /strava/authorize redirects to strava/authorization_successful
# Stores the data from Strava both locally and to MongoDB
@strava_page.route("/strava/authorization_successful")
def authorization_successful():

    params = {
        "client_id": config.strava['STRAVA_CLIENT_ID'],
        "client_secret": config.strava['STRAVA_CLIENT_SECRET'],
        "code": request.args.get('code'),
        "grant_type": "authorization_code"
    }
    
    r = requests.post("https://www.strava.com/oauth/token", params)
    response = json.loads(r.text)

    if 'access_token' in response:
        access_token = response['access_token']
        load_athlete(access_token)
        load_activities(access_token)
        return jsonify({ "message": "Data successfully retrieved" })
    else:
        return jsonify({ "error": "Failed to get access_token" })
    

# Send a parameter in JSON of the ID and get name as a return
# Retrieves from local storage
@strava_page.route('/strava/athlete', methods=['GET'])
def athlete():

    athlete_id = request.get_json()['athlete_id']
    
    try:
        doc = db.strava_athlete_data.find_one({'athlete_id': athlete_id})
        rv = json.dumps({
            'firstname': doc['firstname'],
            'lastname': doc['lastname']
        })

    except Exception as error:
        print(error)
        rv = None

    return jsonify(rv)

# Returns all activity data from athlete ID
# Retrieves from local storage
@strava_page.route("/strava/activities", methods=['GET'])
def activities():

    athlete_id = request.get_json()['athlete_id']
    rv = []
    
    try:
        for doc in db.strava_activity_data.find({'athlete_id': athlete_id}):
            res = json.dumps({
                    'activity_id': doc['activity_id'],
                    'athlete_id': doc['athlete_id'],
                    'start_date': doc['start_date'],
                    'start_date_local': doc['start_date_local'],
                    'distance': doc['distance'],
                    'moving_time': doc['moving_time'],
                    'elapsed_time': doc['elapsed_time'],
                    'type': doc['type']
                })

            rv.append(res)

    except Exception as error:
        print(error)
        rv = None

    return jsonify(rv)

# Return all stored athletes in local storage
@strava_page.route("/strava/athlete_all")
def athlete_all():

    rv = []
    
    try:
        for doc in db.strava_athlete_data.find():
            res = json.dumps({
                'firstname': doc['firstname'],
                'lastname': doc['lastname'],
                'athlete_id': doc['athlete_id']
            })

            rv.append(res)

    except Exception as error:
        print(error)
        rv = None

    return jsonify(rv)


# Load athlete into local storage
def load_athlete(access_token):
    client = StravaIO(access_token)
    athlete = client.get_logged_in_athlete()
    athlete_id = athlete.api_response.id
    f_name = os.path.join(os.path.expanduser('~'), f'.stravadata/athlete_{athlete_id}.json')
    
    if os.path.isfile(f_name):
        # print(f"Athlete {athlete_id}: Already exists locally")

        if db.strava_athlete_data.find({'athlete_id': athlete_id}).count() == 0:
            store_athlete_in_mongo(athlete_id)

    else:
        athlete.store_locally()
        # print(f"Athlete {athlete_id}: Stored locally")
        store_athlete_in_mongo(athlete_id)
        

# Load athletes acitivties into local storage
def load_activities(access_token):

    # Date cariable that sets the lower range for Strava data acquisition  
    get_from_date = config.strava['STRAVA_FETCH_DATA_DATE']
    if get_from_date is None: get_from_date = "2021-04-01"

    client = StravaIO(access_token)
    activities = client.get_logged_in_athlete_activities(after=get_from_date)
    athlete_id = client.get_logged_in_athlete().api_response.id

    for a in activities:
        activity_id = a.id
        activity = client.get_activity_by_id(activity_id)
        f_name = os.path.join(os.path.expanduser('~'), f'.stravadata/activities_{athlete_id}/activity_{activity_id}.json')

        if os.path.isfile(f_name):
            # print(f"Activity {activity_id}: Already exists locally")

            if db.strava_activity_data.find({'activity_id': activity_id}).count() == 0:
                store_activity_in_mongo(athlete_id, activity_id)

        else:
            activity.store_locally() 
            store_activity_in_mongo(athlete_id, activity_id)
            # print(f"Activity {activity_id}: Stored locally")
    
# Submit local athlete data to MongoDB
def store_athlete_in_mongo(athlete_id):

    """Store athlete in MongoDB"""

    dir_name = os.path.join(os.path.expanduser('~'), '.stravadata')
    f_name = os.path.join(dir_name, f"athlete_{athlete_id}.json")

    try:    
        with open(f_name, 'r') as f:
            data = json.load(f)
            res = db.strava_athlete_data.update_one(
                {
                    'athlete_id': data['id']
                }, 
                {
                    "$set":{
                        'firstname': data['firstname'],
                        'lastname': data['lastname'],
                    }
                },    
                upsert = True
                )
            
            """
            if res.matched_count > 0:
                print(f"{data['firstname']} {data['lastname']} already in database")
            elif db.strava_athlete_data.find({'athlete_id': athlete_id}).count() > 0:
                print(f"{data['firstname']} {data['lastname']} uploaded to database")
            else: 
                print("Error when uploading")
            """
            
    except Exception as error:
        print(error)

# Submit local activity data to MongoDB
def store_activity_in_mongo(athlete_id, activity_id):

    """Store activity in MongoDB"""
    
    dir_activities = os.path.join(os.path.expanduser('~'), f'.stravadata/activities_{athlete_id}')
    f_name = os.path.join(dir_activities, f"activity_{activity_id}.json")

    if not os.path.exists(dir_activities):
        return jsonify(f"Directory missing for athlete {athlete_id}")

    try:    
        with open(f_name, 'r') as f:
            data = json.load(f)
            res = db.strava_activity_data.update_one(
                {
                    'activity_id': data['id']
                }, 
                {
                    "$set":{
                        'athlete_id': data['athlete']['id'],
                        'start_date': data['start_date'],
                        'start_date_local': data['start_date_local'],
                        'distance': data['distance'],
                        'moving_time': data['moving_time'],
                        'elapsed_time': data['elapsed_time'],
                        'type': data['type']
                    }
                },    
                upsert = True
                )

            """
            if res.matched_count > 0:
                print(f"Activity {data['id']} already in database")
            elif db.strava_activity_data.find({'activity_id': data['id']}).count() > 0:
                print(f"Activity {data['id']} uploaded to database")
            else: 
                print("Error when uploading")
            """

    except Exception as error:
        print(error)
