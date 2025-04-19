import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecurekey123'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    SQLALCHEMY_DATABASE_URI = 'sqlite:///occur.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
