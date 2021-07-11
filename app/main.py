#utilities
from datetime import datetime
from datetime import timedelta
from datetime import timezone

#Flask framework and managers
#imports the flask framework
from flask import Flask
#Import the restful extension from flask to make rest api easier
from flask_restful import Api
#Imports database handler
from database import database
#imports the login manager 
from database.handler import jwt_manager,login_manager, User
#Nessesary for impilzit token refresh
from flask_jwt_extended import get_jwt, create_access_token, get_jwt_identity, set_access_cookies

#Own utilities
#Handles the audio files and their metadata
from apps.shared.metadata_reader import AudioDirHandler

#Views
#imports the login view
from apps.login.views import login_blueprint
#imports the muscity view
from apps.muscity.views import muscity_blueprint

#Api
from apps.api.ressources.titles import TitlesList
from apps.api.ressources.titles import Titles



def create_app():
    #Creates an Flask application
    app = Flask(__name__)
    #Initizilises the restful object
    api = Api(app)
    #Defines the configuration of the application
    app.config.from_object('config.DevelopmentConfig')    

    #Initializes the database
    database.init_app(app)

    #Initializes the login manager
    login_manager.init_app(app)

    #Initializes the jwt_manager
    jwt_manager.init_app(app)

    #associates the user from the id while a requests is made 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Using an `after_request` callback, we refresh any token that is within 30
    # minutes of expiring. Change the timedeltas to match the needs of your application.
    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original respone
            return response


    #Manages the audio files and adds their metadata to the system
    audio_handler = AudioDirHandler(app)
    
    #registers the login blueprint
    app.register_blueprint(login_blueprint, url_prefix='/')
    #registers the muscity blueprint
    app.register_blueprint(muscity_blueprint, url_prefix='')

    #adds all api ressources
    api.add_resource(TitlesList, '/api/titles')
    api.add_resource(Titles, '/api/titles/<int:id>')

    return app


#Initializes the application
if __name__ == '__main__':
    app = create_app()
    app.run()
    

