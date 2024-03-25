from sqlalchemy import Column, Integer, DateTime, String, Text, inspect

from . import db # from __init__.py

# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html
class TestUser(db.Model):
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
    id  = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(Text, default=None)
    img_url = Column(String(256), nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return "<%r>" % self.email