from flask import Flask, Blueprint, render_template, session, redirect
from database import db
from user.models import User

api_page = Blueprint('api_page', __name__)

