import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OXAPAY_API_KEY = os.environ.get('OXAPAY_API_KEY') or 'your-oxapay-api-key'
