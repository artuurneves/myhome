import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

os.environ['FLASK_ENV'] = 'development'
DEBUG = True

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'myhome.db')
SQLALCHEMY_DATABASE_URI = 'postgres://postgres:mysecretpassword@localhost/myhome'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'MySecret'

