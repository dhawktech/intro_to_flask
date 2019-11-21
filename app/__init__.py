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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app)

  login.init_app(app)
  moment.init_app(app)

  from app.blueprints.account import bp as account_bp
  app.register_blueprint(account_bp, url_prefix='/account')

  from app.blueprints.apis import bp as apis_bp
  app.register_blueprint(apis_bp, url_prefix='/apis')

  with app.app_context():
    from app import routes, models

  return app
