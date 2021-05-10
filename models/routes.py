from flask import Flask, Blueprint, render_template, session, redirect, jsonify, request
from database import db
from bson.json_util import loads, dumps
import requests
import json
import pymongo
import datetime
import config as config 
from models.neural_predictor import HRV_tomorrow

ml_page = Blueprint('ml_page', __name__)

@ml_page.route("/ml/neural", methods=['GET'])
def create_group():

    
    user_id = request.args.get('user_id')

    name = config.user[user_id]
    rv = HRV_tomorrow(name)
    return jsonify(rv[0])

    

# Get HRV value from model [X]
# @ml_page.route('/ml/predict', methods=['GET'])
#def get_hrv():
