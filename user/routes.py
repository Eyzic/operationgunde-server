from flask import Flask, Blueprint, render_template
from database import db
from user.models import User

user_page = Blueprint('user_page', __name__)

@user_page.route('/users/signup/', methods=['POST'])
def signup():
  return User().signup()
 
@user_page.route('/user/signout/')
def signout():
  return User().signout()

@user_page.route('/users/login/', methods=['POST'])
def login():
  return User().login()

@user_page.route('/dashboard/')
def dashboard():
   return render_template('dashboard.html')