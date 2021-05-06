from flask import Flask, Blueprint, render_template, session, redirect, jsonify, request
from database import db
from bson.json_util import loads, dumps
import requests
import json
import pymongo
import datetime

ml_page = Blueprint('ml_page', __name__)

# Get HRV value from model [X]
@ml_page.route('/ml/predict', methods=['GET'])
def get_hrv():


@ml_page.route('/ml/last', methods=['GET'])
def get_last_7_days():

    MULTIPLE = 3

    user_id = request.args.get('user_id')
    nb_activities = request.args.get('nb_activities')

    res_stats = db.stats_form_data.find({ "user_id" : user_id}).sort('date', pymongo.DESCENDING).limit(int(nb_activities)*MULTIPLE)
    res_training = db.training_form_data.find({ "user_id" : user_id}).sort('date', pymongo.DESCENDING).limit(int(nb_activities)*MULTIPLE)

    stats_form = []
    stats_form_arr = []
    training_form = []
    training_form_arr = []

    for doc in res_stats:
        stats_form_arr.append([doc['user_id'],doc['date'],doc['hrv'],doc['sleeping_hours'],doc['muscle_ache'],doc['mood_level'],doc['injury_level'],doc['energy_level']]
        stats_form.append(res)

    for doc in res_training:
        training_form_arr.append([doc['user_id'],doc['date'],doc['energy_level'],doc['elapsed_time'],doc['training_intensity']])
        training_form.append(res)

    rv = []

    for i in range(1,len(stats_form_arr)):
        for j in range(1,len(training_form_arr)):

            y_i, m_i, d_i = stats_form_arr[i][1].split("-")
            y_j, m_j, d_j = training_form_arr[i][1].split("-")

            d1 = datetime.datetime(y_i, m_i, d_i)
            d2 = datetime.datetime(y_j, m_j, d_j)

            
            



    for i in range(1,len(stats_form_arr)):
        for j in range(1,len(training_form_arr)):
            if stats_form_arr[i][1] == training_form_arr[j][1]:
                training_form_arr[j].pop(0)
                training_form_arr[j].pop(1)
                rv.append(stats_form_arr[i] + training_form_arr[j])
            break
            

    #print(stats_form_arr)
    #print(training_form_arr)

    print(rv)

    #return jsonify(rv)

    return jsonify("OK")