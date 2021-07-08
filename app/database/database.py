from flask_sqlalchemy import SQLAlchemy
from database.handler import db

def init_app(app):
    """Initializes the database and creates the models

    Args:
        app (Flask): The context of the application is important so a Flask
                     object has to be provided
    """
    #Provided the app object to the sql_alchemy object
    db.init_app(app)

    #Creates the database models
    db.create_all(app=app)