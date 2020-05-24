import os

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from flask_login import LoginManager

from myhome.extensions.database import db

template_dir = os.path.abspath('./myhome/views/templates')
static_dir = os.path.abspath('./myhome/views/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object('settings')

db.init_app(app=app)
migrate = Migrate(app=app, db=db)

manager = Manager(app=app)
port = int(os.environ.get('PORT', 5000))
manager.add_command('runserver', Server(host='0.0.0.0', port=port))
manager.add_command('db', MigrateCommand)

lm = LoginManager(app)

from myhome.controllers import controller
