from flask import Flask, jsonify, request, session, redirect, render_template
from passlib.hash import pbkdf2_sha256
from database import db
import uuid

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  # Signs up new user and logs in
  def signup(self):
        
    # Create the user object
    # Change from .form.get('name') to .get_json()['name']

    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.user_data.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.user_data.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  # Exits session
  def signout(self):
    session.clear()
    return redirect('/')

  # Log in to system, checks email and (encrypted) password
  def login(self):

    user = db.user_data.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401

  def dashboard(self):
    return render_template('dashboard.html')