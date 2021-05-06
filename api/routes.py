from flask import Flask, Blueprint, render_template, session, redirect, jsonify, request, send_file
from database import db
from bson.json_util import loads, dumps
import requests
import json
import pymongo
import string
import random

api_page = Blueprint('api_page', __name__)

@api_page.route('/index')
def index():
    return {'Test':"Hello world!"}

# Post the stats form (morning form) to database
@api_page.route('/api/form/stats', methods=['POST'])
def post_stats():
    
    # Store parameters from the ge
    json_payload = request.json
    
    params = {'user_id', 'date', 'hrv', 'sleeping_hours', 'stress_level', 'muscle_ache', 'mood_level', 'injury_level', 'energy_level'}
    stats = {}

    for param in params:
        stats[param] = json_payload[param]

    # Checks if 'user_id' and 'date' matches an existing document in the database
    if db.stats_form_data.find({ 'user_id': json_payload['user_id'], 'date': json_payload['date']}).count() > 0:
        return jsonify({ "error": "user and date already registered" })
    
    # Adds the form to the database
    if db.stats_form_data.insert(stats):
        return jsonify({ "message": "insert of stats successful"})

    # If unexpected error occurs, return error
    return jsonify({ "error": "Failed" })


# Get stats based on user_id and date
@api_page.route('/api/form/stats', methods=['GET'])
def get_stats():

    user = request.args.get('user_id')
    date = request.args.get('date')
    
    # Checks if 'user' and 'date' matches an existing document in the database
    if db.stats_form_data.find({"user_id": user, 'date': date}).count() == 0:
          return jsonify({ "error": "can't find user_id and date in database" })

    doc = db.stats_form_data.find_one({ "user_id": user, 'date': date})
    params = {'user_id', 'date', 'hrv', 'sleeping_hours', 'stress_level', 'muscle_ache', 'mood_level', 'injury_level', 'energy_level'}
    stats = {}

    for param in params:
        stats[param] = doc[param]

    return jsonify(stats)


# Delete a stats based on user and date
@api_page.route('/api/form/stats', methods=['DELETE'])
def delete_stats():

    user = request.args.get('user_id')
    date = request.args.get('date')

    # Checks if 'user' and 'date' matches an existing document in the database
    if db.stats_form_data.find({"user_id": user, 'date': date}).count() == 0:
          return jsonify({ "error": "can't find user and date in database" })
    
    # Adds the form to the database
    if db.stats_form_data.delete_many({"user_id": user, 'date': date}).deleted_count > 0:
        return jsonify({ "message": "delete of stats successful"})

    # If unexpected error occurs, return error
    return jsonify({ "error": "Failed" })

# Get stats based on user and date
@api_page.route('/api/form/stats/hrv', methods=['GET'])
def get_stats_hrv():
    
    user = request.args.get('user_id')
    date = request.args.get('date')
    
    # Checks if 'user' and 'date' matches an existing document in the database
    if db.stats_form_data.find({"user_id": user, 'date': date}).count() == 0:
          return jsonify({ "error": "can't find user and date in database" })

    doc = db.stats_form_data.find_one({ "user_id": user, 'date': date}, {'hrv': 1})

    return jsonify(doc['hrv'])


@api_page.route('/api/activity', methods=['POST'])
def post_activity():

    json_payload = request.json

    params = {'user_id', 'title', 'average_heartrate', 'start_date_local', 'distance', 'moving_time', 'elapsed_time', 'type'}
    activity_data = {'activity_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))}

    for param in params:
        activity_data[param] = json_payload[param]
    
    # Adds the form to the database
    if db.activity_data.insert(activity_data):
        return jsonify({ "message": "insert of activity successful"})

    # If unexpected error occurs, return error
    return jsonify({ "error": "Failed" })


# Returns all activity data from athlete ID
@api_page.route("/api/activities", methods=['GET'])
def get_activities():

    user_id = request.args.get('user_id')
    nb_activities = request.args.get('nb_activities', type=int)

    if db.user_data.find({"user_id": user_id}).count() == 0 or isinstance(nb_activities, int) == False or nb_activities < 0:
        return jsonify({ "error": "Undefined query" }), 401

    res = db.user_data.find_one({'user_id': user_id}, {'strava.strava_id' : 1})

    try:
        strava_id = res['strava']['strava_id']
    except: 
        strava_id = ""

    res = db.activity_data.find(
        { "$or" : [
            { "user_id" : user_id },
            { "strava_id" : strava_id }
        ]}
        ).sort('start_date_local', pymongo.DESCENDING).limit(int(nb_activities))

    rv = []

    for doc in res:
            res = {
                    'activity_id': doc['activity_id'],
                    'title': doc['title'],
                    'average_heartrate': doc['average_heartrate'],
                    'start_date_local': doc['start_date_local'],
                    'distance': doc['distance'],
                    'moving_time': doc['moving_time'],
                    'elapsed_time': doc['elapsed_time'],
                    'type': doc['type']
                }

            rv.append(res)

    return jsonify(rv)


# Get training form based on user_id and date
@api_page.route('/api/form/training', methods=['GET'])
def get_form_training():

    user = request.args.get('user_id')
    date = request.args.get('date')
    
    # Checks if 'user' and 'date' matches an existing document in the database
    if db.training_form_data.find({"user_id": user, 'date': date}).count() == 0:
          return jsonify({ "error": "can't find user_id and date in database" })

    doc = db.training_form_data.find_one({ "user_id": user, 'date': date})
    
    params = {'user_id', 'date', 'training_intensity', 'training_type', 'elapsed_time', 'energy_level'}
    stats = {}

    for param in params:
        stats[param] = doc[param]

    return jsonify(stats)



@api_page.route('/api/form/training', methods=['POST'])
def post_form_training():
    
    json_payload = request.json
    
    params = {'user_id', 'date', 'training_intensity', 'training_type', 'elapsed_time', 'energy_level'}
    training_form_data = {}

    for param in params:
        training_form_data[param] = json_payload[param]

    # Checks if 'user' and 'date' matches an existing document in the database
    res = db.training_form_data.find(
        { "$and" : [
            { "user_id" : json_payload['user_id'] },
            { "date" : json_payload['date'] }
        ]}
        )

    if res.count() > 0:
        return jsonify({ "error": "training form already registered" })
    
    # Adds the form to the database
    if db.training_form_data.insert(training_form_data):
        return jsonify({ "message": "insert of training form successful"})

    # If unexpected error occurs, return error
    return jsonify({ "error": "Failed" })

# Create a group
@api_page.route("/api/group", methods=['POST'])
def create_group():

    logo = request.json.get('logo')
    group = request.json.get('group')
   
    res = db.groups.update(
                {
                    'group': group
                }, 
                {
                    '$set':{'logo': logo}
                },
                upsert=True
                )
    if res['nModified'] > 0:
        return jsonify({ "message": "group added successful"})

    return jsonify({ "message": "group not inserted"})


# Add a group to an user
@api_page.route("/api/user/group", methods=['POST'])
def add_group():

    user_id = request.json.get('user_id')
    group = request.json.get('group')

    res = db.groups.update_one({'group' : group}, {'$addToSet':{'members': user_id}}, upsert = True)
    
    return jsonify({ "message": "user added successful"})


# Get an users group and number of members
@api_page.route("/api/user/group", methods=['GET'])
def get_group():
    
    user_id = request.args.get('user_id')
    
    try:
        res = db.groups.find({'members': user_id})
        rv = []
        for doc in res:

            try:
                logo = doc['logo']
            except:
                logo = None

            nb_members = len(doc['members'])
            rv.append([doc['group'], nb_members, logo])

        return jsonify(rv)

    except: 
        return jsonify({ "error": "Input doesn't match with item in database" })

# Get users in a specific group
@api_page.route("/api/group", methods=['GET'])
def get_group_members():

    group = request.args.get('group')

    try:
        res = db.groups.find_one({'group': group})
        ids = res['members']

        rv = []

        for id in ids:
            try:
                name = db.user_data.find_one({'user_id': id})
                rv.append([name['name'], id])
            except:
                pass

        return jsonify(rv)

    except: 
        return jsonify({ "error": "No members of this group" })




"""# Add an organisation to an user
@api_page.route("/api/user/organisation", methods=['POST'])
def add_organisation():

    json_payload = request.json
    
    user_id = json_payload.get('user_id')
    organisation = json_payload.get('organisation')

    res = db.user_data.update(
                {
                    'user_id': user_id
                }, 
                {
                    '$addToSet':{
                        'organisations': organisation
                    }
                }
                )
        
    if res['nModified'] > 0:
        return jsonify({ "message": "organisation added successful"})

    return jsonify({ "message": "organisation already exists"})

@api_page.route("/api/user/organisation", methods=['GET'])
def get_organisation():
    
    user_id = request.args.get('user_id')

    try:
        res = db.user_data.find_one({'user_id': user_id})
        organisations = res['organisation']
        return jsonify(organisations)
    except: 
        return jsonify({ "error": "No organisations for this user" })


@api_page.route("/api/organisation", methods=['GET'])
def get_organisation_members():

    organisation = request.args.get('organisation')
    res = db.user_data.find({'organisations': organisation})

    if res.count() == 0:
        return jsonify({ "error": "No members in this organisation" }), 400

    rv = []

    for doc in res:
        res = {'user_id': doc['user_id'], 'name': doc['name']}
        rv.append(res)
    
    return jsonify(rv)"""

@api_page.route('/get_png', methods=['GET'])
def get_png():

    logo = request.args.get('logo')

    filename = 'logos/' + logo + '.png'
    return send_file(filename, mimetype='image/png')