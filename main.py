from flask import Flask, render_template, Blueprint, redirect
from flask_restful import Api
from bson.json_util import loads, dumps
from flask_cors import CORS
from user.routes import *
from api.routes import *
from strava.routes import *

app = Flask(__name__)
app.register_blueprint(user_page)
app.register_blueprint(api_page)
app.register_blueprint(strava_page)
api = Api(app)
CORS(app)


@app.route("/")
def home():
    return render_template('home.html')

##################################
# Method 1

@app.route("/data")
def data():
    return {"data": "Here is data!"}

if __name__ == "__main__":
    app.secret_key = 'secretkey'
    app.run()



