from os import path
from secrets import randbits


class Config(object):
    # Setup Flask App Config
    DEBUG = False
    TESTING = False
    SECRET_KEY = randbits(64)  # urandom(24)  # specify the length in brackets

    # Setup SQLAlchemy Environment
    SQLDB_FILENAME = 'weather.db'
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + path.join(path.abspath(path.dirname(__file__)), SQLDB_FILENAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DB_USERNAME = 'app_user'
    DB_PASSWORD = '<BLANK>'
    UPLOADS = '/home/username/app/app/static/images/uploads'
    SESSION_COOKIE_SECURE = True


class Production(Config):
    pass


class Development(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class Testing(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
