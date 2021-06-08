#imports the flask framework
from flask import Flask
#Imports database handler
from database import database

#imports the login view
from apps.login.views import login_blueprint

def create_app():
    #Creates an Flask application
    app = Flask(__name__)
    #Defines the configuration of the application
    app.config.from_object('config.DevelopmentConfig')

    #Initializes the database
    database.init_app(app)

    #registers the login blueprint
    app.register_blueprint(login_blueprint, url_prefix='/login')

    return app



if __name__ == '__main__':
    create_app().run()

