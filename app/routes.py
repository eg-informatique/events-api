from app import app

from flask import request, jsonify
import uuid

from . import db
from .models import TestUser
from .models import Event

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/test_users')
def list_all_test_users():
    users = TestUser.query.all()
    response = []
    for user in users: response.append(user.toDict())
    return jsonify(response)

@app.route('/events')
def list_all_events():
    events = Event.query.all()
    response = []
    for event in events : response.append(event.toDict())
    return jsonify(response)