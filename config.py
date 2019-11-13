import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xbe\xc1\xacL]U\x83{\xb7(Spt\xb7D@\r\xb2\xc5\x90A\xf3\x99\x1a'
  # FLASK_APP='run.py'
  # FLASK_DEBUG=1
  # FLASK_ENV='development'
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False