from app import app

from flask import Flask, Response, request, render_template, redirect, jsonify, json
import uuid

from .models import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('./index.html')

#------------------------------Event------------------------------------------

@app.get('/events')
def get_events():
    args = request.args
    page = args.get('page') if 'page' in args else 0
    pages = int(page)*20
    events = Event.query.order_by(Event.start_datetime.asc()).offset(pages).limit(20).all()
    response = []
    for event in events : response.append(event.toDict())
    return jsonify(response)

@app.post('/event')
def add_event():
    data = request.get_json()
    new_event = Event(title=data["title"],  
                      img_url=data["img_url"], 
                      start_datetime=data["start_datetime"], 
                      end_datetime=data["end_datetime"],
                      created=func.now(),
                      prices=data["prices"],
                      description=data["description"],
                      venue=data["venue"],
                      organizer=data["organizer"] )
    
    if len(Event.query.filter(Event.title == data["title"]).all()) > 0:
        return Response({'Conficlt name raised : That event already exists'}), 409, {'ContentType':'application/json'}
    db.session.add(new_event)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/event/<id>')
def get_event(id):
    events = Event.query.filter(Event.id == id).all()
    response=[]
    for event in events : response.append(event.toDict())
    if len(response) == 0:
        return Response({'ERROR 404':True}, 404, {'ContentTypes':'application/json'})
    return jsonify(response)

@app.patch('/event/<id>')
def patch_event(id):
    data = request.get_json()
    event = Event.query.filter(Event.id == id).first_or_404()
    event.title = data["title"]
    event.img_url = data["img_url"]
    event.start_datetime = data["start_datetime"]
    event.end_datetime = data["end_datetime"]
    event.prices = data["prices"]
    event.description = data["description"]
    event.venue = data["venue"]
    event.organizer = data["organizer"]
    db.session.commit()
    return Response({'success':True}), 202, {'ContentType':'application/json'}

@app.delete('/event/<id>')
def delete_event(id):
    event = Event.query.filter(Event.id == id).first_or_404()
    db.session.delete(event)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'} 

#------------------------------Venue------------------------------------------

@app.route('/venues')
def get_venues():
    args = request.args
    page = args.get('page') if 'page' in args else 0
    pages = int(page)*20
    venues = Venue.query.offset(pages).limit(20).all()
    response = []
    for venue in venues : response.append(venue.toDict())
    return jsonify(response)

@app.route('/venue/<id>')
def get_venue(id):
    venues = Venue.query.filter(Venue.id == id).all()
    response = []
    for venue in venues : response.append(venue.toDict())
    if len(response) == 0:
        return Response({'ERROR 404':True}, 404, {'ContentTypes':'application/json'})
    return jsonify(response)

@app.post('/venue')
def post_venue():
    data = request.get_json()
    new_venue = Venue(name=data["name"], 
                      url=data["url"], 
                      address=data["address"], 
                      zipcode=data["zipcode"], 
                      city=data["city"],
                      country=data["country"],
                      email=data["email"],
                      phone=data["phone"]
                      )
    if len(Venue.query.filter(Venue.name == data["name"]).all()) > 0:
        return Response({'That venue already exists, try to patch this venue if the infos are not up to date'}), 409, {'ContentType':'application/json'}
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
    venue.email = data["email"]
    venue.phone = data["phone"]
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
    page = args.get('page') if 'page' in args else 0
    pages = int(page)*20
    users = AppUser.query.offset(pages).limit(20).all()
    response = []
    for user in users : response.append(user.toDict())
    return jsonify(response)

@app.route('/user/<id>')
def get_user(id):
    users = AppUser.query.filter(AppUser.id == id).all()
    response = []
    for user in users : response.append(user.toDict())
    if len(response) == 0:
        return Response({'ERROR 404':True}), 404, {'ContentTypes':'application/json'}
    return jsonify(response)

@app.post('/user')
def post_user():
    data = request.get_json()
    new_user = AppUser(first_name=data["first_name"], 
                      last_name=data["last_name"],
                      email=data["email"],
                      password=data["password"]
                      )
    if len(AppUser.query.filter(AppUser.email == data["email"]).all()) > 0:
        return Response({'Email already used'}), 409, {'ContentType':'application/json'}
    if len(AppUser.query.filter(AppUser.first_name == data["first_name"]).all()) > 0 and len(AppUser.query.filter(AppUser.last_name == data["last_name"]).all()):
        return Response({'This user already exists'}), 409, {'ContentType':'application/json'}
    db.session.add(new_user)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'}

@app.patch('/user/<id>')
def patch_user(id):
    data = request.get_json()
    user = AppUser.query.filter(AppUser.id == id).first_or_404()
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.email = data["email"]
    user.password = data["password"]
    db.session.commit()
    return Response({'success':True}), 202, {'ContentType':'application/json'}

@app.delete('/user/<id>')
def delete_user(id):
    user = AppUser.query.filter(AppUser.id == id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'}

@app.get('/user')
def getUserByEmail():
    email = request.args.get('email')
    if not email:
        return jsonify({'massage': 'Email is required'}), 400
    
    user = AppUser.query.filter(AppUser.email==email).first()
    if user:
        return jsonify({'exists': True, 'user': {'id': user.id, 'email': user.email}})
    else: 
        return jsonify({'exists': False}), 404
#------------------------------Acount gestion--------------------------------------

@app.post('/login')
def verify_user():
    data = request.get_json()
    user = AppUser.query.filter(AppUser.email == data["email"]).first_or_404()
    if user.verify_password(data["password"]):
        return jsonify({'id': user.id, 'email':user.email}), 200
    else: 
        return Response({'authenticated':False}), 401,{'ContentType': 'application/json'}