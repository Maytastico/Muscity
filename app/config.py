import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'f~0@2Gr_&KvE(H"7SV4A.{wB[vA`M=ZY2poPw`?='
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="sqlite:///app_data.db"