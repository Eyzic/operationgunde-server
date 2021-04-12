from flask import Flask, Blueprint, render_template, session, redirect, jsonify, request
from database import db
from bson.json_util import loads, dumps
import json

api_page = Blueprint('api_page', __name__)

@api_page.route('/index')
def index():
    return {'Test':"Hello world!"}

# Post the stats form (morning form) to database
@api_page.route('/api/stats', methods=['POST'])
def post_stats():
    
    # Store parameters from the ge
    json_payload = request.get_json()
    
    params = {'user', 'date', 'hrv', 'sleeping_hours', 'stress_level', 'muscle_ache', 'mood_level', 'injury_level', 'energy_level'}
    stats = {}

    for param in params:
        stats[param] = json_payload[param]

    # Checks if 'user' and 'date' matches an existing document in the database
    if db.stats_data.find({ "user": json_payload['user'], 'date': json_payload['date']}).count() > 0:
          return jsonify({ "error": "user and date already registered" })
    
    # Adds the form to the database
    if db.stats_data.insert(stats):
        return jsonify({ "message": "insert of stats successful"})

    # If unexpected error occurs, return error
    return jsonify({ "error": "Failed" })


# Get stats based on user and date
@api_page.route('/api/stats', methods=['GET'])
def get_stats():

    data = request.get_json()
    user = data['user']
    date = data['date']
    
    # Checks if 'user' and 'date' matches an existing document in the database
    if db.stats_data.find({"user": user, 'date': date}).count() == 0:
          return jsonify({ "error": "can't find user and date in database" })

    doc = db.stats_data.find_one({ "user": user, 'date': date})
    params = {'user', 'date', 'hrv', 'sleeping_hours', 'stress_level', 'muscle_ache', 'mood_level', 'injury_level', 'energy_level'}
    stats = {}

    for param in params:
        stats[param] = doc[param]

    return jsonify(stats)


# Delete a stats based on user and date
@api_page.route('/api/stats', methods=['DELETE'])
def delete_stats():

    data = request.get_json()
    user = data['user']
    date = data['date']

    # Checks if 'user' and 'date' matches an existing document in the database
    if db.stats_data.find({"user": user, 'date': date}).count() == 0:
          return jsonify({ "error": "can't find user and date in database" })
    
    # Adds the form to the database
    if db.stats_data.delete_many({"user": user, 'date': date}).deleted_count > 0:
        return jsonify({ "message": "delete of stats successful"})

    # If unexpected error occurs, return error
    return jsonify({ "error": "Failed" })

# Get stats based on user and date
@api_page.route('/api/stats/hrv', methods=['GET'])
def get_stats_hrv():
    
    data = request.get_json()
    user = data['user']
    date = data['date']
    
    # Checks if 'user' and 'date' matches an existing document in the database
    if db.stats_data.find({"user": user, 'date': date}).count() == 0:
          return jsonify({ "error": "can't find user and date in database" })

    doc = db.stats_data.find_one({ "user": user, 'date': date}, {'hrv': 1})

    return jsonify(doc['hrv'])


@api_page.route('/api/training', methods=['POST'])
def post_training():
    
    json_payload = request.get_json()
    
    params = {'user', 'activity_id' 'training_intensity', 'training_type', 'training_duration', 'energy_level'}
    training_data = {}

    for param in params:
        training_data[param] = json_payload[param]

    # Checks if 'user' and 'date' matches an existing document in the database
    if db.training_data.find({ "activity_id": json_payload['activity_id']}).count() > 0:
          return jsonify({ "error": "activity already registered" })
    
    # Adds the form to the database
    if db.training_data.insert(training_data):
        return jsonify({ "message": "insert of activity successful"})

    # If unexpected error occurs, return error
    return jsonify({ "error": "Failed" })