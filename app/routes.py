from app import app
from datetime import datetime
from flask import Flask, Response, request, render_template, redirect, jsonify, abort, json, send_file
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from fpdf import FPDF
import os
import uuid
import jwt
from sqlalchemy import or_, and_
import sys



from .models import *

mail = Mail(app)

JWT_SECRET = 'polosecrets'

def verify_jwt(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        abort(401, "Token expired")
    except jwt.InvalidTokenError:
        abort(401, "Invalid token")



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
    sort = args.get("sort")
    date_str = args.get("d")
    event_creator = args.get("c")
    events_query = Event.query
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        events_query = events_query.filter(Event.start_datetime >= date)
    if sort == 'ascending':
        events_query = events_query.order_by(Event.start_datetime.asc())
    else:
        events_query = events_query.order_by(Event.start_datetime.desc())
    search_query = args.get("search", "").strip()
    if search_query and search_query != "":
        events_query = events_query.filter(
            or_(
                Event.title.ilike(f'%{search_query}%'),
                Event.description.ilike(f'%{search_query}%')
            )
        )
    if event_creator:
        events_query = events_query.filter(Event.organizer == event_creator)
    events_query = events_query.offset(pages).limit(12)
    events = events_query.all()
    response = []
    for event in events : response.append(event.toDict())
    return jsonify(response)


@app.post('/event')
def add_event():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    data = request.form.to_dict()
    
    if not file or file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    ext = os.path.splitext(file.filename)[1]  # Get file extension
    unique_filename = f"{os.path.splitext(file.filename)[0]}_{uuid.uuid4().hex}{ext}"
    filename = secure_filename(unique_filename)
    file_path = os.path.join('/var/www/', filename)
    file.save(file_path)
    file_url = f"https://events-api.org/static/{filename}"

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
    reservations = Events_AppUsers.query.filter(Events_AppUsers.event == id).all()
    event = Event.query.filter(Event.id == id).first_or_404()
    img_url = event.img_url
    file_path = f"/var/www/{img_url[30:]}"
    if os.path.isfile(file_path):
        os.remove(file_path)
    if reservations:
        for reservation in reservations:
            db.session.delete(reservation)
            db.session.commit()
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
    venue_creator = args.get("c")
    if search_query:
        venue_query = venue_query.filter(
            or_(
                Venue.name.ilike(f'%{search_query}%'),
                Venue.address.ilike(f'%{search_query}%'),
                Venue.city.ilike(f'%{search_query}%')
            )
        )
    if venue_creator:
        venue_query = venue_query.filter(Venue.creator == venue_creator)
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
                      phone=data["phone"],
                      creator = data["creator"]
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
    venue.address = data["address"]
    venue.zipcode = data["zipcode"]
    venue.city = data["city"]
    venue.country = data["country"]
    venue.email = data["email"]
    venue.phone = data["phone"]
    db.session.commit()
    return Response({'success':True}), 202, {'ContentType':'application/json'} 

@app.delete('/venue/<id>')
def delete_venue(id):
    events = Event.query.filter(Event.venue == id).all()
    venue = Venue.query.filter(Venue.id == id).first_or_404()
    if events:
        for event in events:
            db.session.delete(event)
            db.session.commit()
    db.session.delete(venue)
    db.session.commit()
    return Response({'success':True}), 200, {'ContentType':'application/json'} 

#------------------------------Users------------------------------------------

@app.get('/users')
def get_users():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(" ")[1]
        decoded_token = verify_jwt(token)
        if decoded_token:
            args = request.args
            page = args.get('page') if 'page' in args else 0
            pages = int(page)*20
            users = AppUser.query.offset(pages).limit(20).all()
            response = []
            for user in users : response.append(user.toDict())
            return jsonify(response)
    return abort(401, "Authorization required")
    

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
        return jsonify({"error": "Email already used"}), 409
    
    db.session.add(new_user)
    db.session.commit()
    try:
        response = send_verification_email(new_user.email, new_user.email_token, new_user.id)
        if response[0]: 
            return jsonify({f"success":True}), 200
        else:
            db.session.delete(new_user)
            db.session.commit()
            return jsonify({f"Unsuccess - In mail sending, error: {response[1]}":True}), 500
    except Exception as e:
        db.session.delete(new_user)
        db.session.commit()
        return jsonify({f'{e}': True}), 500

def send_verification_email(email, token, id):
    try:
        verification_link = f"https://swiss-events.org/verify-email?id={id}&token={token}"
        subject = "Verify Your Email Address"
        
        with open("/home/tm/events-api/app/email_template.html", "r") as file:
            html_template = file.read()
        html_body = html_template.replace("{{ verification_link }}", verification_link)
 
        msg = Message(subject, recipients=[email])
        msg.body = "Please verify your email using the following link: " + verification_link
        msg.html = html_body

        mail.send(msg)

    except Exception as e:
        return [False, str(e)]
    return [True, '123']

@app.get('/send-verification-email')
def send_to_app_verification_email():
    email = request.args.get("email")
    user = AppUser.query.filter(AppUser.email == str(email)).first()
    id = user.id
    email_token = user.email_token
    try:
        response = send_verification_email(email, email_token, id)
        if response[0]: 
            return Response({f"success":True}), 200, {'ContentType':'application/json'}
        else:
            return Response({f"Unsuccess - In mail sending, error: {response[1]}":True}), 500, {'ContentType':'application/json'}
    except Exception as e:
        return Response({f'{e}': True}), 500, {'application/json'}
    

@app.patch('/user/<id>')
def patch_user(id):
    data = request.get_json()
    user = AppUser.query.filter(AppUser.id == id).first_or_404()
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
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
        return jsonify({'exists': True, 'user': {'id': user.id, 'email': user.email, 'first_name':user.first_name, 'verify':user.verify}})
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

@app.post('/verify-email')
def verify_email():
    data = request.get_json()
    id = data["id"]
    token = data["token"]

    user = AppUser.query.filter(AppUser.id == id).first_or_404()
    if user.email_token == token:
        user.verify = True
        db.session.commit()
        return jsonify('ok'), 202, {'ContentType':'application/json'}
    else:
        return Response({'unsuccess':True}), 400, {'ContentType':'application/json'}


#------------------------------Event reservation--------------------------------------


@app.post('/reserve/<eventId>/<usrId>/<nb_tickets>')
def reserve_event(eventId, usrId, nb_tickets):
    reservations = Events_AppUsers.query
    reservations = reservations.filter(Events_AppUsers.app_user == usrId)
    reservations = reservations.filter(Events_AppUsers.event == eventId)
    is_reserve_exists = reservations.first()
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

@app.patch('/reserve/<eventId>/<usrId>/<nb_tickets>')
def edit_reservation(eventId, usrId, nb_tickets):
    reservation = Events_AppUsers.query.filter(and_(Events_AppUsers.event == eventId, Events_AppUsers.app_user == usrId)).first_or_404()
    reservation.nb_tickets = nb_tickets
    if int(reservation.nb_tickets) - int(nb_tickets) == 0:
        db.session.delete(reservation)
    db.session.commit()
    return Response({'success':True}), 202, {'ContentType':'application/json'}

@app.get('/app_user_list/<id>')
def appUser_list(id):
    reservationList = Events_AppUsers.query.filter(Events_AppUsers.event == id).all()
    if len(reservationList) == 0:
        return jsonify({'exists': False}), 404
    userList = [i.toDict().get("app_user") for i in reservationList]

    return jsonify(userList), 200

@app.get('/event_list/<id>')
def event_list(id):
    reservationList = Events_AppUsers.query.filter(Events_AppUsers.app_user == id).all()
    if len(reservationList) == 0:
        return jsonify({'exists': False}), 404
    eventList = [i.toDict().get("event") for i in reservationList]
    return jsonify(eventList), 200

@app.get('/event_nb_tickets/<eventId>/<usrId>')
def get_nb_tickets(eventId, usrId):
    reservation = Events_AppUsers.query.filter(and_(Events_AppUsers.event == eventId), (Events_AppUsers.app_user == usrId)).first()
    nb_tickets = reservation.toDict().get("nb_tickets")
    return jsonify(nb_tickets), 200
 
#--------------------------PDF------------------------------
@app.get('/registred-events-pdf')
def get_registred_pdf():
    event_id = request.args.get('event_id')
    event = Event.query.filter(Event.id == event_id).first()
    reservationList = Events_AppUsers.query.filter(Events_AppUsers.event == event_id).all()
    if len(reservationList) == 0:
        return jsonify({'exists': False}), 404
    registredList = [i.toDict().get("app_user") for i in reservationList]
    
    ticket_tot = sum(i.nb_tickets for i in reservationList)
    
    pdf = FPDF()
    pdf.add_page()

    logo_path = '/home/tm/events-api/app/logo.png'
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=30)

    # Titre principal
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, f"Registered List for {event.title}", ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, f"Total Tickets: {ticket_tot}", ln=True, align='C')
    pdf.ln(20)

    # Tableau des inscrits
    pdf.set_font('Arial', '', 10)
    pdf.set_fill_color(200, 220, 255)
    alternating_color = False

    pdf.cell(50, 10, "First Name", border=1, align='C', fill=True)
    pdf.cell(50, 10, "Last Name", border=1, align='C', fill=True)
    pdf.cell(70, 10, "Email", border=1, align='C', fill=True)
    pdf.cell(20, 10, "Tickets", border=1, align='C', fill=True)
    pdf.ln()

    for reg in registredList:
        registration = next((i for i in reservationList if i.app_user == reg), None)
        user = AppUser.query.filter(AppUser.id == reg).first()
        pdf.set_fill_color(245 if alternating_color else 255)
        pdf.cell(50, 10, user.first_name, border=1, fill=True)
        pdf.cell(50, 10, user.last_name, border=1, fill=True)
        pdf.cell(70, 10, user.email, border=1, fill=True)
        pdf.cell(20, 10, str(registration.nb_tickets), border=1, fill=True)
        pdf.ln()
        alternating_color = not alternating_color

    pdf_path = f"/tmp/{event.title.replace(' ', '_')}_registered_list.pdf"
    pdf.output(pdf_path)

    return send_file(pdf_path, as_attachment=True, download_name=f"{event.title}-registered-list.pdf")