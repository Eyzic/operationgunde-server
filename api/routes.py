from flask import Flask, Blueprint, render_template, session, redirect
from database import db

api_page = Blueprint('api_page', __name__)

@api_page.route('/index', methods=["GET"])
def index():
    return jsonify(message="Hello world!"), 200

@api_page.route('/data', methods=['GET'])
def get_activity_data(person):
    person = db.activity_data
    return jsonify('X')

@api_page.route('/hrv', methods=['POST'])
def put_hrv(activity):
    json_payload = request.get_json()
    
    hrv_data = db.hrv_data
    
    hrv_form = hrv_data.insert(
        {
            '_id':
            'hrv':
            'sleeping_hours':
            'stress_level':
            'muscle_ache':
            'mood_level':
            'injury_level':
            'energy_level':
        }

@api_page.route('/training', methods=['POST'])
def put_training(activity):
    json_payload = request.get_json()
    training_data = db.training_data
    
    test_data = {
            '_id': 'Filip',
            'training_intensity': 1,
            'training_type': 'Konditionsträning',
            'training_duration': 50,
            'energy_level': 7,
        }

    training_form = training_data.insert(
        {
            '_id': test_data.get('_id'),
            'training_intensity': test_data.get('training_intensity'),
            'training_type': test_data.get('training_type'),
            'training_duration': test_data.get('training_duration'),
            'energy_level': test_data.get('energy_level')
        }

@api_page.route('/activity', methods=['POST'])
def put_activity(activity):
    json_payload = request.get_json()
    user_entry = User.

    activity = db.activity_data
    
    activities = activity.insert(
        {
            '_id': 
            'start_time':
            'end_time':
            'name':
            'type':
            'athlete_id':
            'sensor_data':
                            {
                                'type': 
                                'value':
                                'timestamp':
                            }
        }
    )
    