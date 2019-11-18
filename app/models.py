from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  email = db.Column(db.String(60), unique=True)
  password = db.Column(db.String(120))
  posts = db.relationship('Post', backref='author', lazy='dynamic')

  def generate_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def __repr__(self):
    return f'<User: {self.name} | {self.email}>'

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return f"<Post: {self.user_id}: {self.body[:20]}>"

@login.user_loader
def load_user(id):
  # SELECT * FROM user WHERE id = ?
  return User.query.get(id)