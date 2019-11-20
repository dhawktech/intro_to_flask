from flask import Blueprint, render_template, redirect, url_for, flash
from app.blueprints.account.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

bp = Blueprint('account', __name__, template_folder='templates')

@bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data):
      flash("Incorrect email or password. Try again.", "danger")
      return redirect(url_for('account.login'))
    login_user(user, remember=form.remember_me.data)
    flash("You have logged in successfully", "success")
    return redirect(url_for('about'))
  context = {
    'form': form
  }
  return render_template('account/login.html', **context)

@bp.route('/register', methods=['GET', 'POST'])
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

@bp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('account.login'))