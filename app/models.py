from sqlalchemy import Column, Integer, DateTime, Date, Boolean, String, Text, ForeignKey,inspect

from . import db # from __init__.py

# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html
class TestUser(db.Model):
    """
    Test entity
    """
    #name of the table in database
    __tablename__="test_user"

    id           = db.Column(Integer, primary_key=True, autoincrement=True)
    email        = db.Column(db.String(64), nullable=False, unique=True)
    name     = db.Column(db.String(64), nullable=False)

    # How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return "<%r>" % self.email
    
class Event(db.Model):
    """
    Event 

    See https://schema.org/Event
    """
    __tablename__="event"

    id  = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(256), nullable=False)
    # TODO: add description field
    img_url = Column(String(256), nullable=True)
    # TODO: rename start_date -> start_datetime
    start_date = Column(DateTime(timezone=True), nullable=False)
    # TODO: rename end_date -> end_datetime
    end_date = Column(DateTime(timezone=True), nullable=False)
    # TODO: rename venue_id -> venue. Foreign key is indeed venue.id
    # NB: this is a one to one relationship
    venue_id = Column(Integer, ForeignKey('venue.id'))
    event_details = db.relationship('EventDetails', backref="oneevent")
    
    # TODO: add created and updated fields (automatically updated)
    # Date of event creation 
    #created      = db.Column(db.DateTime(timezone=True), default=datetime.now)                           
    # Date of event last update 
    #updated      = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)   

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Venue(db.Model):
    """
    Event venue
    
    See https://schema.org/EventVenue
    """
    __tablename__ = "venue"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(64), nullable = False)
    # TODO: add description field
    url = Column(Text, default=None)
    # TODO: rename adress -> address
    adress = Column(String(64), nullable=False)
    # TODO: add email field
    # TODO: add phone field
    zipcode = Column(String(64), nullable=False)
    city = Column(String(64), nullable=False)
    country = Column(String(64), nullable=False)
    # TODO: add location field (latitude and longitude) -> see PostGIS extension
    # TODO: remove field 'event'. For now, 'venue_id' in Event table is OK 
    events = db.relationship('Event', backref='venue')

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

# TODO: rename Users -> User    
class Users(db.Model):
    """
    User
    """
    # TODO: rename users -> user
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # TODO: rename firstname -> first_name
    firstname = Column(String(64), nullable=False)
    # TODO: rename lastname -> last_name
    lastname = Column(String(64), nullable=False)
    # TODO: rename pseudo -> username / nullable=False
    pseudo = Column(String(16), nullable=True, default=None)
    # TODO: rename birthdate -> birth_date
    birthdate = Column(Date, nullable=False)
    email = Column(String(64), nullable=False)
    # TODO: add mobile field
    # TODO: add password_hash field

    # TODO: field to be removed
    event_details = db.relationship('EventDetails', backref='users')

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class EventDetails(db.Model):
    """
    Event details
    """
    __tablename__ = "event_details"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    event = Column(Integer, ForeignKey('event.id'))
    # TODO: rename price -> prices / should be reprensented as a JSON value. 
    # Something like {'minor': 10, 'major': 20, 'currency': 'EUR'}
    price = Column(Integer, nullable=True)
    # TODO: remove this field for now
    attendes = Column(Integer, nullable=False)
    # TODO: remove filed 'description'. For now, 'description' in Event table is OK
    description = Column(Text, nullable=False)
    organizer = Column(Integer, ForeignKey('users.id'))

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
