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
    print(f"Authorize url = {rv}")
    
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
    
# Connects a user_id with a Strava strava_id
@strava_page.route("/strava/connect", methods=['POST'])
def connect_athlete():

    json_payload = request.json

    user_id = json_payload.get('user_id')
    strava_id = json_payload.get('strava_id')
    doc = db.strava_athlete_data.find_one({'strava_id': strava_id})

    try:
        db.user_data.update(
            {
                'user_id': user_id
            }, 
            {
                "$set":{
                    'strava.strava_id': strava_id,
                    'strava.firstname': doc['firstname'],
                    'strava.lastname': doc['lastname']
                }
            }
            )

        a = db.user_data.find_one({ "user_id" : {"$eq" : user_id } } )['_id']
        b = db.user_data.find_one({ "strava.strava_id" : {"$eq" : strava_id } } )['_id']

        if a == b:
            return jsonify({ "message": "athlete_id and user_id connected"})

        return jsonify({ "message": "athlete_id or user_id did not exist"})

    except Exception as error:
        return jsonify({ "error": "athlete_id or user_id did not exist"})

# Send a parameter in JSON of the ID and get name as a return
# Retrieves from local storage
@strava_page.route('/strava/athlete', methods=['GET'])
def athlete():

    strava_id = request.args.get('strava_id')
    
    try:
        doc = db.strava_athlete_data.find_one({'strava_id': strava_id})
        rv = {
            'firstname': doc['firstname'],
            'lastname': doc['lastname']
        }

    except Exception as error:
        print(error)
        rv = None

    return jsonify(rv)

# Return all stored athletes in local storage
@strava_page.route("/strava/athlete_all", methods=['GET'])
def athlete_all():

    rv = []
    
    try:
        for doc in db.strava_athlete_data.find():
            res = {
                'firstname': doc['firstname'],
                'lastname': doc['lastname'],
                'strava_id': doc['strava_id']
            }

            rv.append(res)

    except Exception as error:
        print(error)
        rv = None

    return jsonify(rv)