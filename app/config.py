import os
from datetime import timedelta

class Config(object):
    #Flask config parameters
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    JWT_COOKIE_CSRF_PROTECT = False
    SECRET_KEY = 'WQ7zs08OYSFe9OO1ZmTRgpGqiZo3k5j3'
    JWT_SECRET_KEY = 'f~0@2Gr_&KvE(H"7SV4A.{wB[vA`M=ZY2poPw`?='
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Application config parameters
    FILE_DIR = os.getcwd() + '/music'
    ARTIST_COVER_DIR = FILE_DIR + '/artist_cover'
    TITLE_COVER_DIR = FILE_DIR + '/title_cover'
    ALBUM_COVER_DIR = FILE_DIR + '/album_cover'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    JWT_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="sqlite:///app_data.db"
    JWT_COOKIE_SECURE = False