import os
from flask import Flask
from dotenv import load_dotenv
from .app_db import db, migrate
from flask_cors import CORS

def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    
    from . import models

    return app