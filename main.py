from flask import Flask
from flask_restful import Api, Resource
from pymongo import MongoClient
import config.keys as config 


client = MongoClient(config.mongodb["mongo_URI"])
db = client.get_database('Test')
sensor_data = db.sensor_data

app = Flask(__name__)
api = Api(app)

@app.route("/")
def home():
    greeting = "Hello, this is some sample text!"
    return str(list(sensor_data.find())[0]['value']) 

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



