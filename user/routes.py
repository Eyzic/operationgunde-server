from flask import Flask, Blueprint, render_template, session, redirect
from database import db
from user.models import User

user_page = Blueprint('user_page', __name__)

@user_page.route('/user/signup/', methods=['POST'])
def signup():
  return User().signup()
 
@user_page.route('/user/signout/')
def signout():
  return User().signout()

@user_page.route('/user/login/', methods=['POST'])
def login():
  return User().login()

'''
def login_required(f):
    @wraps(f)s
    def wrap(*arg, **kwarg):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
'''

@user_page.route('/dashboard')
# @login_required
def dashboard():
   return render_template('dashboard.html')

