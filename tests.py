from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post
from config import DevelopmentConfig

class TestConfig:
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///'

class UserModelCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_password_hashing(self):
    u = User(name='Coding')
    u.generate_password('abc123')
    self.assertFalse(u.check_password('123abc'))
    self.assertTrue(u.check_password('abc123'))

  def test_follow(self):
    u1 = User(name="John", email="johndoe@email.com")
    u2 = User(name="Jane", email="janedoe@email.com")
    db.session.add_all([u1, u2])
    db.session.commit()
    self.assertEqual(u1.followed.all(), [])
    self.assertEqual(u2.followed.all(), [])

    u1.follow(u2)
    db.session.commit()
    self.assertTrue(u1.is_following(u2))
    self.assertEqual(u1.followed.count(), 1)
    self.assertEqual(u1.followed.first().name, "Jane")
    self.assertEqual(u2.followers.count(), 1)
    self.assertEqual(u2.followers.first().name, "John")

    u1.unfollow(u2)
    db.session.commit()
    self.assertFalse(u1.is_following(u2))
    self.assertEqual(u1.followed.count(), 0)
    self.assertEqual(u2.followers.count(), 0)

if __name__ == '__main__':
  unittest.main(verbosity=2)