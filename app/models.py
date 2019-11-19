from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

followers = db.Table(
  'followers',
  db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  email = db.Column(db.String(60), unique=True)
  password = db.Column(db.String(120))
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  followed = db.relationship(
    'User',
    secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
  )

  def follow(self, user):
    if not self.is_following(user):
      self.followed.append(user)
      db.session.commit()

  def unfollow(self, user):
    if self.is_following(user):
      self.followed.remove(user)
      db.session.commit()

  def followed_posts(self):
    followed = Post.query.join(
        followers, 
        (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc()
      )
    own = Post.query.filter_by(user_id=self.id)
    return followed.union(own).order_by(Post.timestamp.desc())


  def is_following(self, user):
    return self.followed.filter(followers.c.followed_id == user.id).count() > 0

  def generate_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def __repr__(self):
    return f'<User: {self.name} | {self.email}>'

  def __str__(self):
    return self.name

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