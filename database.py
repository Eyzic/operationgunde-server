from flask import Flask
from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy

import config as config 

# NoSQL database
client = MongoClient(config.mongodb["URI"])
db = client.get_database('Test')
sensor_data = db.sensor_data

# SQL database
sql_db = SQLAlchemy(app)