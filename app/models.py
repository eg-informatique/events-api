from sqlalchemy import Column, Integer,Enum, String, inspect

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
class evenements(db.model):
	idevenement = Column(Integer(unsigned=True),autoincrement=True, nullable=False)
	idLieu = Column(Integer(unsigned=True), default=0, nullable=False)
	idSalle = Column(Integer, default=0, nullable=False)
	idPersonne = Column(Integer(unsigned=True),default=0, nullable=False)
	statut = Column(enum("actif","inactif","annule","complet","propose"),default="actif", nullable=False)
	genre = Column(Varchar(20),default="divers", nullable=False)
	titre = Column(Varchar(120),default="", nullable=False)
	dateEvenement = Column(date,default="0000-00-00", nullable=False)
	nomLieu = Column(Varchar(255),default="autre", nullable=False)
	adresse = Column(String, nullable=False)
	quartier = Column(Varchar(255),default="autre", nullable=False)
	localite_id = Column(Varchar(6),Nullable=False)
	region = Column(Varchar(2), nullable=False)
	urlLieu = Column(Varchar(255),default="", nullable=False)
	horaire_debut = Column(datetime,default="0000-00-00", nullable=False)
	horaire_fin = Column(datetime,default="0000-00-00", nullable=False)
	horaire_complement = Column(varchar(120),default="", nullable=False)
	description = Column(Integer, nullable=False)
	flyer = Column(varchar(255),default="", nullable=False)
	image = Column(varchar(255),default="", nullable=False)
	price_type = Column(varchar(40), nullable=False)
	prix = Column(varchar(255),default="", nullable=False)
	prelocations = Column(varchar(80),default="", nullable=False)
	ref = Column(varchar(255),default="", nullable=False)
	remarque = Column(Integer, default=Null)
	user_email = Column(varchar(255),default=Null)
	dateAjoute = Column(datetime,default="0000-00-00 00:00:00", nullable=False)
	date_derniere_modif = Column(datetime,default="0000-00-00 00:00:00", nullable=False)
