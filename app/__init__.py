from flask import Flask
import os
from config import Config

basedir = os.path.abspath(os.path.dirname(__file__))

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_migrate import Migrate
migrate = Migrate()

from flask_login import LoginManager
login = LoginManager()
login.login_view = 'account.login'
login.login_message_category = 'info'

from flask_moment import Moment
moment = Moment()

def create_app(config_class=Config):
  app = Flask(__name__)
  if os.environ['FLASK_ENV'] == 'development':
    FLASK_DEBUG=1
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  elif os.environ['FLASK_ENV'] == 'production':
    FLASK_DEBUG=0
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
  elif os.environ['FLASK_ENV'] == 'test':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app)

  login.init_app(app)
  moment.init_app(app)

  from app.blueprints.users import users
  app.register_blueprint(users, url_prefix='/users')

  from app.blueprints.account import account
  app.register_blueprint(account, url_prefix='/account')

  from app.blueprints.apis import apis
  app.register_blueprint(apis, url_prefix='/apis')

  from app.blueprints.main import main
  app.register_blueprint(main, url_prefix='/')

  with app.app_context():
    from app import routes, errors

  return app