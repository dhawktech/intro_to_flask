from flask import Flask
import os

app = Flask(__name__)

from config import ProductionConfig, DevelopmentConfig
if os.environ['FLASK_ENV'] == 'development':
  app.config.from_object(DevelopmentConfig)
elif os.environ['FLASK_ENV'] == 'production':
  app.config.from_object(ProductionConfig)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)

from flask_login import LoginManager
login = LoginManager(app)
login.login_view = 'login'

from flask_moment import Moment
moment = Moment(app)

from flask_mail import Mail
mail = Mail(app)

from app import routes, models