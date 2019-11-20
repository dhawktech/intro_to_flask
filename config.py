import os
basedir = os.path.abspath(os.path.dirname(__file__))

class ProductionConfig:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'sqlite:///'
  SQLALCHEMY_TRACK_MODIFICATIONS = False