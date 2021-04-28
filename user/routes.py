from flask import Flask, jsonify, request, session, redirect, render_template, Blueprint
from database import db
from passlib.hash import pbkdf2_sha256
import uuid

user_page = Blueprint('user_page', __name__)

@user_page.route('/signup', methods=['POST'])
def signup():
      
    # Create the user object

    user = {
        'user_id': uuid.uuid4().hex,
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.user_data.find_one({ "email" : user['email'] }):
        return jsonify({ "error" : "Email address already in use" })

    if db.user_data.insert_one(user):
        return jsonify({ "user_id" : user['user_id']})

    return jsonify({ "error" : "Signup failed" })

"""
@user_page.route('/signout', methods=['POST'])
def signout():
      
    user = db.user_data.find_one({
            'user_id' : request.json['user_id']
        })

    if user:
        db.user_data.update(
            {
                'user_id': user['user_id']
            },
            {
                "$set":{
                    'user_id': uuid.uuid4().hex
                }
            }
            )
        return jsonify({ "message" : "User successfully signed out" })
        
    return jsonify({ "error": "User doesn't exist" })
"""

@user_page.route('/login', methods=['POST'])
def login():
      
    user = db.user_data.find_one({
            "email": request.json['email']
        })

    if user and pbkdf2_sha256.verify(request.json['password'], user['password']):
            return jsonify({ "user_id" : user['user_id']})
        
    return jsonify({ "error": "Invalid login credentials" }), 401
