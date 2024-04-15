from sqlalchemy import Column, Integer, DateTime, Date, Boolean, String, Text, ForeignKey,inspect

from . import db # from __init__.py

# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html
class TestUser(db.Model):
    #name of the table in database
    __tablename__="test_user"

    # auto-generated fields
    id           = db.Column(Integer, primary_key=True, autoincrement=True)
    #created      = db.Column(db.DateTime(timezone=True), default=datetime.now)                           # The Date of the Instance Creation => Created one Time when Instantiation
    #updated      = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)    # The Date of the Instance Update => Changed with Every Update

    # Input by User Fields:
    email        = db.Column(db.String(64), nullable=False, unique=True)
    name     = db.Column(db.String(64), nullable=False)

    # How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return "<%r>" % self.email
    
class Event(db.Model):
    __tablename__="event"

    id  = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(256), nullable=False)
    img_url = Column(String(256), nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    venue_id = Column(Integer, ForeignKey('venue.id'))
    event_details = db.relationship('EventDetails', backref="oneevent")

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Venue(db.Model):
    __tablename__ = "venue"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(64), nullable = False)
    url = Column(Text, default=None)
    adress = Column(String(64), nullable=False)
    zipcode = Column(String(64), nullable=False)
    city = Column(String(64), nullable=False)
    country = Column(String(64), nullable=False)
    events = db.relationship('Event', backref='venue')

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
class Users(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    firstname = Column(String(64), nullable=False)
    lastname = Column(String(64), nullable=False)
    pseudo = Column(String(16), nullable=True, default=None)
    birthdate = Column(Date, nullable=False)
    email = Column(String(64), nullable=False)
    event_details = db.relationship('EventDetails', backref='users')

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class EventDetails(db.Model):
    __tablename__ = "event_details"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    event = Column(Integer, ForeignKey('event.id'))
    price = Column(Integer, nullable=True)
    attendes = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    organizer = Column(Integer, ForeignKey('users.id'))

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
