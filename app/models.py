from sqlalchemy import Column, Integer, DateTime, Date, JSON, String, Text, ForeignKey, func, inspect
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from geoalchemy2 import Geometry


from . import db # from __init__.py
 
class Event(db.Model):
    """
    Event 

    See https://schema.org/Event
    """
    __tablename__="event"

    id  = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # Title of the event
    title = Column(String(256), nullable=False)
    # Url of the image of the event
    img_url = Column(String(256), nullable=True)
    # Start datetime of the event 
    start_datetime = Column(DateTime(timezone=True), nullable=False)
    # End datetime of the event 
    end_datetime = Column(DateTime(timezone=True), nullable=False)
    # NB: this is a one to one relationship
    venue = Column(Integer, ForeignKey('venue.id'))
    event_details = db.relationship('EventDetails', backref="oneevent")
    # Date of event creation 
    created = Column(DateTime(timezone=True), default=func.now())                           
    # Date of event last update 
    update = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())   

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Venue(db.Model):
    """
    Event venue
    
    See https://schema.org/EventVenue
    """
    __tablename__ = "venue"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # Name of the venue
    name = Column(String(64), nullable = False)
    # Url of the venue
    url = Column(Text, default=None)
    # Address of the venue
    address = Column(String(64), nullable=False)
    # Zipcode of the venue
    zipcode = Column(String(64), nullable=False)
    # City of the venue
    city = Column(String(64), nullable=False)
    # Country of the venue
    country = Column(String(64), nullable=False)
    # Email of the venue
    email = Column(String(64), nullable=False)
    # Phone number of the venue
    phone = Column(String(64), nullable=False)
    # TODO: add location field (latitude and longitude) -> see PostGIS extension
    # events = db.relationship('Event', backref='venue')

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

  
class AppUser(db.Model):
    """
    App User

    See => https://schema.org/Person
    """
    
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # First name of the user
    first_name = Column(String(64), nullable=False)
    # Last name of the user
    last_name = Column(String(64), nullable=False)
    # Username of the user
    username = Column(String(64), nullable=False)
    # Birth date of the user
    birth_date = Column(Date, nullable=False)
    # Email of the user
    email = Column(String(64), nullable=False)
    # Phone number of the user
    mobile = Column(String(64), nullable=False)
    # Password of user => https://youtu.be/8ebIEefhBpM?si=qburaQAyHBxueuzN
    password_hash = Column(String(256), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attibute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class EventDetails(db.Model):
    """
    Event details
    """
    __tablename__ = "event_details"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # Id of the event that is detailed
    event = Column(Integer, ForeignKey('event.id'))
    # Price of the event
    # Something like {'minor': 10, 'major': 20, 'currency': 'EUR'}
    prices = Column(JSON, nullable=True)
    # Description of the event
    description = Column(Text, nullable=False)
    #Id of the user that organize the event
    organizer = Column(Integer, ForeignKey('app_user.id'))

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
