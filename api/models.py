from flask import Flask, jsonify, request, session, redirect, render_template
from database import db

class Activity(db.activity):
    
    def __init__(self, id, username, password):
