from flask import Flask
from pymongo import MongoClient
import config as config 
from stravaio import strava_oauth2


# NoSQL database
client = MongoClient(config.mongodb["URI"])
db = client.get_database('Test')

# Strava API database
oauth2 = strava_oauth2(client_id=config.strava['client_id'], client_secret=config.strava['client_secret'])
config.strava['access_token'] = oauth2
