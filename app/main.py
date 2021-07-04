#imports the flask framework
from flask import Flask
#Imports database handler
from database import database
#imports the login manager 
from database.models import login_manager, User

#imports the login view
from apps.login.views import login_blueprint

#imports the muscity view
from apps.muscity.views import muscity_blueprint

def create_app():
    #Creates an Flask application
    app = Flask(__name__)
    #Defines the configuration of the application
    app.config.from_object('config.DevelopmentConfig')

    #Initializes the database
    database.init_app(app)

    #Initializes the login manager
    login_manager.init_app(app)

    #associates the user from the id 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #registers the login blueprint
    app.register_blueprint(login_blueprint, url_prefix='/')
    
    #registers the muscity blueprint
    app.register_blueprint(muscity_blueprint, url_prefix='/muscity')

    return app



if __name__ == '__main__':
    create_app().run()

