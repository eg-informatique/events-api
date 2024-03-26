from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import config

db = SQLAlchemy()
migrate = Migrate()

# CONFIF_MODE = os.getenv("CONFIG_MODE")
CONFIG_MODE = 'development'

app = Flask(__name__, template_folder='template')
    
app.config.from_object(config[CONFIG_MODE])

db.init_app(app)
migrate.init_app(app, db)

from app import routes
