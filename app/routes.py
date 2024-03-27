from app import app

from flask import Flask, Response, request, render_template, redirect, jsonify, json
import uuid

from .models import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('./index.html')

@app.route('/test_users')
def list_all_test_users():
    users = TestUser.query.all()
    response = []
    for user in users: response.append(user.toDict())
    return jsonify(response)

@app.route('/event')
def list_all_events():
    events = Event.query.all()
    response = []
    for event in events : response.append(event.toDict())
    return jsonify(response)

@app.post('/event')
def add_event():
    data = request.get_json()
    new_event = Event(title=data["title"], 
                      description=data["description"], 
                      img_url=data["img_url"], 
                      start_date=data["start_date"], 
                      end_date=data["end_date"])
    db.session.add(new_event)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'} 