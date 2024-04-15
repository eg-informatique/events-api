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

#------------------------------Event------------------------------------------

@app.get('/events')
def get_events():
    args = request.args
    limit = args.get('limit') if 'limit' in args else 20
    offset = args.get('offset') if 'offset' in args else 0
    page = int(offset)*int(limit)
    events = Event.query.offset(page).limit(limit).all()
    response = []
    for event in events : response.append(event.toDict())
    return jsonify(response)

@app.post('/event')
def add_event():
    data = request.get_json()
    new_event = Event(title=data["title"],  
                      img_url=data["img_url"], 
                      start_date=data["start_date"], 
                      end_date=data["end_date"],
                      venue_id=data["venue_id"])
    db.session.add(new_event)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/event/<id>')
def get_event(id):
    events = Event.query.filter(Event.id == id).all()
    response=[]
    for event in events : response.append(event.toDict())
    if len(response) == 0:
        return Response({'ERROR':True}, 404, {'ContentTypes':'application/json'})
    return jsonify(response)

@app.patch('/event/<id>')
def patch_event(id):
    data = request.get_json()
    event = Event.query.filter(Event.id == id).first_or_404()
    event.title = data["title"]
    event.img_url = data["img_url"]
    event.start_date = data["start_date"]
    event.end_date = data["end_date"]
    db.session.commit()
    return Response({'success':True}), 202, {'ContentType':'application/json'}

@app.delete('/event/<id>')
def delete_event(id):
    event = Event.query.filter(Event.id == id).first_or_404()
    event_details = EventDetails.query.filter(EventDetails.event == id).first_or_404()
    db.session.delete(event_details)
    db.session.delete(event)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'} 

#------------------------------Venue------------------------------------------

@app.route('/venues')
def get_venues():
    args = request.args
    limit = args.get('limit') if 'limit' in args else 20
    offset = args.get('offset') if 'offset' in args else 0
    page = int(offset)*int(limit)
    venues = Venue.query.offset(page).limit(limit).all()
    response = []
    for venue in venues : response.append(venue.toDict())
    return jsonify(response)

@app.route('/venue/<id>')
def get_venue(id):
    venues = Venue.query.filter(Venue.id == id).all()
    response = []
    for venue in venues : response.append(venue.toDict())
    if len(response) == 0:
        return Response({'ERROR':True}, 404, {'ContentTypes':'application/json'})
    return jsonify(response)

@app.post('/venue')
def post_venue():
    data = request.get_json()
    new_venue = Venue(name=data["name"], 
                      url=data["url"], 
                      adress=data["adress"], 
                      zipcode=data["zipcode"], 
                      city=data["city"],
                      country=data["country"],
                      )
    db.session.add(new_venue)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'} 

@app.patch('/venue/<id>')
def patch_venue(id):
    data = request.get_json()
    venue = Venue.query.filter(Venue.id == id).first_or_404()
    venue.name = data["name"]
    venue.url = data["url"]
    venue.adress = data["adress"]
    venue.zipcode = data["zipcode"]
    venue.city = data["city"]
    venue.country = data["country"]
    db.session.commit()
    return Response({'success':True}), 202, {'ContentType':'application/json'} 

@app.delete('/venue/<id>')
def delete_venue(id):
    venue = Venue.query.filter(Venue.id == id).first_or_404()
    db.session.delete(venue)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'} 

#------------------------------Users------------------------------------------

@app.get('/users')
def get_users():
    args = request.args
    limit = args.get('limit') if 'limit' in args else 20
    offset = args.get('offset') if 'offset' in args else 0
    page = int(offset)*int(limit)
    users = Users.query.offset(page).limit(limit).all()
    response = []
    for user in users : response.append(user.toDict())
    return jsonify(response)

@app.route('/user/<id>')
def get_user(id):
    users = Users.query.filter(Users.id == id).all()
    response = []
    for user in users : response.append(user.toDict())
    if len(response) == 0:
        return Response({'ERROR':True}, 404, {'ContentTypes':'application/json'})
    return jsonify(response)

@app.post('/user')
def post_user():
    data = request.get_json()
    new_user = Users(lastname=data["lastname"], 
                      firstname=data["firstname"], 
                      pseudo=data["pseudo"], 
                      birthdate=data["birthdate"], 
                      email=data["email"]
                      )
    db.session.add(new_user)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'}

@app.patch('/user/<id>')
def patch_user(id):
    data = request.get_json()
    user = Users.query.filter(Users.id == id).first_or_404()
    user.lastname = data["lastname"]
    user.firstname = data["firstname"]
    user.pseudo = data["pseudo"]
    user.birthdate = data["birthdate"]
    user.email = data["email"]
    db.session.commit()
    return Response({'success':True}), 202, {'ContentType':'application/json'}

@app.delete('/user/<id>')
def delete_user(id):
    user = Users.query.filter(Users.id == id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'}

#------------------------------Event_details------------------------------------------

@app.route('/event_details/<id>')
def get_eventDetails(id):
    event_details = EventDetails.query.filter(EventDetails.event == id).all()
    response = []
    for event in event_details : response.append(event.toDict())
    if len(response) == 0:
        return Response({'ERROR':True}, 404, {'ContentTypes':'application/json'})
    return jsonify(response)

@app.post('/event_details/')
def post_eventDetails():
    data = request.get_json()
    new_eventDetails = EventDetails(event=data["event"], 
                                    price=data["price"], 
                                    attendes=data["attendes"], 
                                    description=data["description"], 
                                    organizer=data["organizer"]
                      )
    db.session.add(new_eventDetails)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'}

@app.patch('/event_details/<id>')
def patch_eventDetails(id):
    data = request.get_json()
    event_details = EventDetails.query.filter(EventDetails.event == id).first_or_404()
    event_details.price = data["price"]
    event_details.attendes = data["attendes"]
    event_details.description = data["description"]
    event_details.organizer = data["organizer"]
    db.session.commit()
    return Response({'success':True}), 202, {'ContentType':'application/json'}

@app.delete('/event_details/<id>')
def delete_eventDetails(id):
    event_details = EventDetails.query.filter(EventDetails.event == id).first_or_404()
    db.session.delete(event_details)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'}
