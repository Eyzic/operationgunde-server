from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

@app.route("/")
def home():
    return "Hello, this is some sample text!"

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