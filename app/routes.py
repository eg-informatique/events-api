from app import app

from flask import Flask, request, render_template, redirect,jsonify
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

@app.route('/events')
def list_all_events():
    events = Event.query.all()
    response = []
    for event in events : response.append(event.toDict())
    return jsonify(response)

@app.route('/add_event', methods=['GET', 'POST'])
def post_event():
    if request.method == 'GET':
        return render_template('addEvent.html')
    new_event = Event(title=request.form["title"], description=request.form["description"], img_url=request.form["img_url"], start_date=request.form["start_date"], end_date=request.form["end_date"])
    db.session.add(new_event)
    db.session.commit()
    return redirect('/events')