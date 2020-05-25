import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

os.environ['FLASK_ENV'] = 'development'
DEBUG = True

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'myhome.db')
# SQLALCHEMY_DATABASE_URI = 'postgres://postgres:artur@localhost/myhome'
SQLALCHEMY_DATABASE_URI = 'postgres://hdbvtyownacjxu:e26d738473129da93cc22faec2a1e900cac70f8179bc4ec281d4891d57a5dda1@ec2-50-17-90-177.compute-1.amazonaws.com:5432/d3pgdibg062s1r'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'MySecret'

