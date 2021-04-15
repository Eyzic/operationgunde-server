from flask import Flask, Blueprint, render_template, session, redirect, jsonify, request
from database import db
from bson.json_util import loads, dumps
import requests

api_page = Blueprint('api_page', __name__)

@api_page.route('/index')
def index():
    return {'Test':"Hello world!"}

# Post the stats form (morning form) to database
@api_page.route('/api/stats', methods=['POST'])
def post_stats():
    
    # Store parameters from the ge
    json_payload = request.json
    
    params = {'user_id', 'date', 'hrv', 'sleeping_hours', 'stress_level', 'muscle_ache', 'mood_level', 'injury_level', 'energy_level'}
    stats = {}

    for param in params:
        stats[param] = json_payload.get(param)

    # Checks if 'user_id' and 'date' matches an existing document in the database
    if db.stats_data.find({ 'user_id': json_payload['user_id'], 'date': json_payload['date']}).count() > 0:
        return jsonify({ "error": "user and date already registered" })
    
    # Adds the form to the database
    if db.stats_data.insert(stats):
        return jsonify({ "message": "insert of stats successful"})

    # If unexpected error occurs, return error
    return jsonify({ "error": "Failed" })


# Get stats based on user_id and date
@api_page.route('/api/stats', methods=['GET'])
def get_stats():

    user = request.args.get('user_id')
    date = request.args.get('date')
    
    # Checks if 'user' and 'date' matches an existing document in the database
    if db.stats_data.find({"user_id": user, 'date': date}).count() == 0:
          return jsonify({ "error": "can't find user_id and date in database" })

    doc = db.stats_data.find_one({ "user_id": user, 'date': date})
    params = {'user_id', 'date', 'hrv', 'sleeping_hours', 'stress_level', 'muscle_ache', 'mood_level', 'injury_level', 'energy_level'}
    stats = {}

    for param in params:
        stats[param] = doc[param]

    return jsonify(stats)


# Delete a stats based on user and date
@api_page.route('/api/stats', methods=['DELETE'])
def delete_stats():

    user = request.args.get('user_id')
    date = request.args.get('date')

    # Checks if 'user' and 'date' matches an existing document in the database
    if db.stats_data.find({"user_id": user, 'date': date}).count() == 0:
          return jsonify({ "error": "can't find user and date in database" })
    
    # Adds the form to the database
    if db.stats_data.delete_many({"user_id": user, 'date': date}).deleted_count > 0:
        return jsonify({ "message": "delete of stats successful"})

    # If unexpected error occurs, return error
    return jsonify({ "error": "Failed" })

# Get stats based on user and date
@api_page.route('/api/stats/hrv', methods=['GET'])
def get_stats_hrv():
    
    user = request.args.get('user_id')
    date = request.args.get('date')
    
    # Checks if 'user' and 'date' matches an existing document in the database
    if db.stats_data.find({"user_id": user, 'date': date}).count() == 0:
          return jsonify({ "error": "can't find user and date in database" })

    doc = db.stats_data.find_one({ "user_id": user, 'date': date}, {'hrv': 1})

    return jsonify(doc['hrv'])


@api_page.route('/api/training', methods=['POST'])
def post_training():
    
    json_payload = request.json
    
    params = {'user_id', 'activity_id' 'training_intensity', 'training_type', 'training_duration', 'energy_level'}
    training_data = {}

    for param in params:
        training_data[param] = json_payload.get(param)

    # Checks if 'user' and 'date' matches an existing document in the database
    if db.training_data.find({ "activity_id": json_payload['activity_id']}).count() > 0:
          return jsonify({ "error": "activity already registered" })
    
    # Adds the form to the database
    if db.training_data.insert(training_data):
        return jsonify({ "message": "insert of activity successful"})

    # If unexpected error occurs, return error
    return jsonify({ "error": "Failed" })


# Add a group to an user
@api_page.route("/api/group", methods=['POST'])
def add_group():

    json_payload = request.json

    user_id = json_payload.get('user_id')
    group = json_payload.get('group')
    
    res = db.user_data.update(
                {
                    'user_id': user_id
                }, 
                {
                    '$addToSet':{
                        'groups': group
                    }
                }
                )

    if res['nModified'] > 0:
        return jsonify({ "message": "group added successful"})

    return jsonify({ "message": "group not inserted"})

# Add an organisation to an user
@api_page.route("/api/organisation", methods=['POST'])
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
