from flask import Flask
from pymongo import MongoClient

import config as config 

# NoSQL database
client = MongoClient(config.mongodb["URI"])
db = client.get_database('Test')
sensor_data = db.sensor_data
