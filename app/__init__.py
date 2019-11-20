import os
from flask import Flask
from config import Config

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
  app.config.from_object(config_class)
  
  db.init_app(app)
  migrate.init_app(app, db)
  
  login.init_app(app)
  moment.init_app(app)

  from app.blueprints.account import bp as account_bp
  app.register_blueprint(account_bp, url_prefix='/account')

  with app.app_context():
    from app import routes, models

  return app
