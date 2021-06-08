from flask_sqlalchemy import SQLAlchemy
from .models import db

def init_app(app):
    db.init_app(app)
    db.create_all(app=app)