from flask import render_template, redirect, url_for, flash
from app.models import User
from flask_login import login_required, current_user
from app.blueprints.users import users

@users.route('/')
def index():
  context = {
    'users': [i for i in User.query.all() if i.id != current_user.id],
  }
  return render_template('users/index.html', **context)

@users.route('/add/<user>')
@login_required
def add(user):
  user = User.query.filter_by(name=user).first()
  if user not in current_user.followed:
    current_user.follow(user)
    flash("User added successfully", "success")
    return redirect(url_for('users.index'))
  flash(f"You are already following {user.name}", "warning")
  return redirect(url_for('users.index'))

@users.route('/remove/<user>')
@login_required
def remove(user):
  user = User.query.filter_by(name=user).first()
  if user in current_user.followed:
    current_user.unfollow(user)
    flash("User removed successfully", "info")
    return redirect(url_for('users.index'))
  flash("You cannot unfollow someone you're not following. Make it make sense, sis...", "danger")
  return redirect(url_for('users.index'))

@users.route('/delete/<user>')
@login_required
def delete(user):
  user = current_user
  db.session.delete(user)
  db.session.commit()
  flash("Your account was deleted successfully. Sorry to see you go.", "info")
  return redirect(url_for('users.index'))