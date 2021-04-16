import config as config 
from stravaio import StravaIO
from stravaio import strava_oauth2
from database import *
import numpy
import requests
import urllib3
import os.path
import json

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

# Load athlete into local storage
def load_athlete(access_token):
    client = StravaIO(access_token)
    athlete = client.get_logged_in_athlete()
    strava_id = str(athlete.api_response.id)
    f_name = os.path.join(os.path.expanduser('~'), f'.stravadata/athlete_{strava_id}.json')
    
    if os.path.isfile(f_name):
        #print(f"Athlete {strava_id}: Already exists locally")

        if db.strava_athlete_data.find({'strava_id': strava_id}).count() == 0:
            store_athlete_in_mongo(strava_id)

    else:
        athlete.store_locally()
        #print(f"Athlete {strava_id}: Stored locally")
        store_athlete_in_mongo(strava_id)
        

# Load athletes acitivties into local storage
def load_activities(access_token):

    # Date cariable that sets the lower range for Strava data acquisition  
    get_from_date = config.strava['STRAVA_FETCH_DATA_DATE']
    if get_from_date is None: get_from_date = "2021-04-01"

    client = StravaIO(access_token)
    activities = client.get_logged_in_athlete_activities(after=get_from_date)
    strava_id = client.get_logged_in_athlete().api_response.id

    for a in activities:
        activity_id = a.id
        activity = client.get_activity_by_id(activity_id)
        f_name = os.path.join(os.path.expanduser('~'), f'.stravadata/activities_{strava_id}/activity_{activity_id}.json')

        if os.path.isfile(f_name):
            #print(f"Activity {activity_id}: Already exists locally")

            if db.activity_data.find({'activity_id': activity_id}).count() == 0:
                store_activity_in_mongo(strava_id, activity_id)

        else:
            activity.store_locally() 
            store_activity_in_mongo(strava_id, activity_id)
            #print(f"Activity {activity_id}: Stored locally")
    
# Submit local athlete data to MongoDB
def store_athlete_in_mongo(strava_id):

    """Store athlete in MongoDB"""

    dir_name = os.path.join(os.path.expanduser('~'), '.stravadata')
    f_name = os.path.join(dir_name, f"athlete_{strava_id}.json")

    try:    
        with open(f_name, 'r') as f:
            data = json.load(f)
            res = db.strava_athlete_data.update_one(
                {
                    'strava_id': str(data['id'])
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
            elif db.strava_athlete_data.find({'strava_id': strava_id}).count() > 0:
                print(f"{data['firstname']} {data['lastname']} uploaded to database")
            else: 
                print("Error when uploading")
            """
            
    except Exception as error:
        print(error)

# Submit local activity data to MongoDB
def store_activity_in_mongo(strava_id, activity_id):

    """Store activity in MongoDB"""
    
    dir_activities = os.path.join(os.path.expanduser('~'), f'.stravadata/activities_{strava_id}')
    f_name = os.path.join(dir_activities, f"activity_{activity_id}.json")

    if not os.path.exists(dir_activities):
        return jsonify(f"Directory missing for athlete {strava_id}")

    try:    
        with open(f_name, 'r') as f:
            data = json.load(f)
            res = db.activity_data.update_one(
                {
                    'activity_id': str(data['id'])
                }, 
                {
                    "$set":{
                        'strava_id': str(data['athlete']['id']),
                        'title': data['name'],
                        'average_heartrate': 0,
                        'start_date_local': data['start_date_local'][0:10],
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
            elif db.activity_data.find({'activity_id': data['id']}).count() > 0:
                print(f"Activity {data['id']} uploaded to database")
            else: 
                print("Error when uploading")
            """

    except Exception as error:
        print(error)


