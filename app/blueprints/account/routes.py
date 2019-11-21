from app import db
from flask import render_template, redirect, url_for, flash
from app.blueprints.main.forms import BlogForm
from app.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.account import account
from app.blueprints.account.forms import LoginForm, RegistrationForm, ProfileForm

# /profile/
@account.route('/profile/<name>', methods=['GET', 'POST'])
@login_required
def profile(name):
  form = BlogForm()
  if form.validate_on_submit():
    p = Post(body=form.body.data, user_id=current_user.id)
    db.session.add(p)
    db.session.commit()
    flash("Post added successfully", 'success')
    return redirect(url_for('account.profile', name=name))
  context = {
    'form': form,
    'posts': Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc()).all()
  }
  return render_template('account/profile.html', **context)

@account.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data):
      flash("Incorrect email or password. Try again.", "danger")
      return redirect(url_for('account.login'))
    login_user(user, remember=form.remember_me.data)
    flash("You have logged in successfully", "success")
    return redirect(url_for('main.about'))
  context = {
    'form': form
  }
  return render_template('account/login.html', **context)

@account.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    u = User(
      name=form.name.data,
      email=form.email.data,
      password=form.password.data
    )
    u.generate_password(u.password)
    db.session.add(u)
    db.session.commit()
    login_user(u)
    flash("You have registered successfully", "info")
    return redirect(url_for('account.login'))
  context = {
    'form': form
  }
  return render_template('account/register.html', **context)

@account.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('account.login'))