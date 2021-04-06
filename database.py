from flask import Flask
from pymongo import MongoClient
import config as config 

# make a connection with MongoDB
try:
    client = MongoClient(config.mongodb["URI"])
    db = client.get_database('Test')
except: 
    print("Could not connect to MongoDB") 
