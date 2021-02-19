from flask import Flask
from flask_restful import Api, Resource
from pymongo import MongoClient
import config.keys as config 
from bson.json_util import loads, dumps
from flask_cors import CORS

client = MongoClient(config.mongodb["URI"])
db = client.get_database('Test')
sensor_data = db.sensor_data

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route("/")
def home():
    return "Hello, this is some sample text!"

@app.route("/database")
def database():
    item = list(sensor_data.find())[0]
    json_item = dumps(item)
    return json_item 

@app.route("/<name>")
def user(name):
    return "Hello " + name

##################################
#Method 1

@app.route("/data")
def data():
    return {"data": "Here is data!"}


##################################
# Method 2

#class Data(Resource):
 #   def get(self):
  #      return {"data": "Here is data!"}

#api.add_resource(Data, "/data")

if __name__ == "__main__":
    app.run()



