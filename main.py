from flask import Flask, render_template, Blueprint, redirect
from flask_restful import Api
from bson.json_util import loads, dumps
from flask_cors import CORS
from user.routes import *


app = Flask(__name__)
app.register_blueprint(user_page)
api = Api(app)
CORS(app)


@app.route("/")
def home():
    return render_template('home.html')

#################################
# Database

@app.route("/database")
def database():
    item = list(sensor_data.find())[0]
    json_item = dumps(item)
    return json_item 

##################################
# Method 1

@app.route("/data")
def data():
    return {"data": "Here is data!"}

if __name__ == "__main__":
    app.secret_key = 'secretkey'
    app.run()



