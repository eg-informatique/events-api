from app import app

from flask import Flask, Response, request, render_template, redirect, jsonify, json
from werkzeug.utils import secure_filename
import os
import uuid
from sqlalchemy import or_


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
    pages = int(page)*12
    events_query = Event.query.order_by(Event.start_datetime.asc())
    search_query = args.get("search", "").strip()
    if search_query and search_query != "":
        events_query = events_query.filter(
            or_(
                Event.title.ilike(f'%{search_query}%'),
                Event.description.ilike(f'%{search_query}%')
            )
        )
    events_query = events_query.offset(pages).limit(12)
    events = events_query.all()
    response = []
    for event in events : response.append(event.toDict())
    return jsonify(response)


@app.post('/event')
def add_event():
    # Check for file in request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    data = request.form.to_dict()
    
    # Validate file and UUID
    if not file or file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Generate a unique filename
    ext = os.path.splitext(file.filename)[1]  # Get file extension
    unique_filename = f"{os.path.splitext(file.filename)[0]}_{uuid.uuid4().hex}{ext}"
    filename = secure_filename(unique_filename)
    file_path = os.path.join('/var/www/', filename)
    file.save(file_path)
    file_url = f"https://events-api.org/static/{filename}"

    # Create event object
    try:
        new_event = Event(
            title=data["title"],
            img_url=file_url,
            start_datetime=data["start_datetime"],
            end_datetime=data["end_datetime"],
            created=func.now(),
            prices={"major":data["major_price"], "minor":data["minor_price"], "currency":"CHF"},
            description=data["description"],
            venue=data["venue"],
            organizer=data["organizer"]
        )
    except:
        if os.path.isfile(file_path):
            os.remove(file_path)
        return jsonify({"Error":True}), 500
    if len(Event.query.filter(Event.title == data["title"]).all()) > 0:
        return jsonify({'Name Conflict':True}), 409

    
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'success':True}), 200


@app.route('/event/<id>')
def get_event(id):
    event = Event.query.filter(Event.id == id).first_or_404()
    event_data = event.toDict()
    return jsonify(event_data)

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
    img_url = event.img_url
    file_path = f"/var/www/{img_url[30:]}"
    if os.path.isfile(file_path):
        os.remove(file_path)
    db.session.delete(event)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'} 

@app.get('/nb_events')
def get_nb_events():
    all_events = Event.query.all()
    return Response({f"{len(all_events)}":True}), 200

#------------------------------Venue------------------------------------------

@app.get('/venues')
def get_venues():
    args = request.args
    page = args.get('page') if 'page' in args else 0
    pages = int(page)*8
    search_query = args.get("search", "").strip()
    venue_query = Venue.query
    if search_query:
        venue_query = venue_query.filter(
            or_(
                Venue.name.ilike(f'%{search_query}%'),
                Venue.address.ilike(f'%{search_query}%'),
                Venue.city.ilike(f'%{search_query}%')
            )
        )
    venue_query = venue_query.offset(pages).limit(6)
    venues = venue_query.all()
    response = []
    for venue in venues : response.append(venue.toDict())
    return jsonify(response), 200

@app.route('/venue/<id>')
def get_venue(id):
    venue = Venue.query.filter(Venue.id == id).first_or_404()
    venue_data = venue.toDict()
    return jsonify(venue_data), 200

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
        return jsonify({'Name Conflict':True}), 409
    db.session.add(new_venue)
    db.session.commit()
    return jsonify({'success':True}), 200 

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
    user = AppUser.query.filter(AppUser.id == id).first_or_404()
    user_data= user.toDict()
    return jsonify(user_data)

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
        return jsonify({'exists': True, 'user': {'id': user.id, 'email': user.email, 'first_name':user.first_name}})
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


#------------------------------Event reservation--------------------------------------


@app.post('/reserve/<eventId>/<usrId>/<nb_tickets>')
def reserve_event(eventId, usrId, nb_tickets):
    is_reserve_exists = Events_AppUsers.query.filter(Events_AppUsers.event == eventId and Events_AppUsers == usrId).first()
    if is_reserve_exists:
        is_reserve_exists.nb_tickets += int(nb_tickets)
        db.session.commit()
        return Response({'success':True}), 200, {'ContentType':'application/json'}
    else:
        new_reservation = Events_AppUsers(
            event = eventId,
            app_user = usrId,
            nb_tickets = nb_tickets
        )

        db.session.add(new_reservation)
        db.session.commit()
        return Response({'success':True}), 200, {'ContentType':'application/json'}

@app.get('/app_user_list/<id>')
def appUser_list(id):
    reservationList = Events_AppUsers.query.filter(Events_AppUsers.event == id).all()
    if len(reservationList) == 0:
        return Response({"no user":True}), 204
    userList = [i.toDict().get("app_user") for i in reservationList]

    return jsonify(userList), 200

@app.get('/event_list/<id>')
def event_list(id):
    reservationList = Events_AppUsers.query.filter(Events_AppUsers.app_user == id).all()
    if len(reservationList) == 0:
        return Response({"no event":True}), 204
    eventList = [i.toDict().get("event") for i in reservationList]

    return jsonify(eventList), 200
