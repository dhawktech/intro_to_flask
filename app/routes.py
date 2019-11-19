from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import RegistrationForm, LoginForm, ProfileForm, BlogForm, ContactForm
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from app.email import send_email

# Made a small change somewhere

# FLASK_LOGIN
# .is_authenticated
# .is_active
# .is_anonymous
# .get_id()

# CRUD APPLICATION
# C - CREATE: POST
# R - READ: GET
# U - UPDATE: PUT
# D - DELETE: DELETE

@app.context_processor
def getGlobal():
  return dict(
    g_username=""
  )

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
  form = BlogForm()
  context = {
    'form': form,
    'posts': Post.query.order_by(Post.timestamp.desc()).all()
  }
  if form.validate_on_submit():
    p = Post(body=form.body.data, user_id=current_user.id)
    db.session.add(p)
    db.session.commit()
    flash("Post added successfully", 'success')
    return redirect(url_for('index'))
  return render_template('index.html', **context)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
  context = {
    'form': form
  }
  if form.validate_on_submit():
    send_email()
    flash("Your form submission was successful", "info")
    return redirect(url_for('contact'))
  return render_template('contact.html', **context)

@app.route('/about', methods=['GET', 'POST'])
@login_required
def about():
  form = ProfileForm()
  context = {
    'form': form
  }
  if request.method == 'GET':
    form.name.data = current_user.name
    form.email.data = current_user.email
  if form.validate_on_submit():
    current_user.name = form.name.data
    current_user.email = form.email.data
    current_user.password = form.password.data
    current_user.generate_password(current_user.password)
    db.session.commit()
    flash('Profile information updated successfully', 'success')
    return redirect(url_for('about'))
  return render_template('about.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data):
      flash("Incorrect email or password. Try again.", "danger")
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    flash("You have logged in successfully", "success")
    return redirect(url_for('about'))
  context = {
    'form': form
  }
  return render_template('login.html', **context)

@app.route('/register', methods=['GET', 'POST'])
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
    flash("You have registered successfully", "info")
    return redirect(url_for('login'))
  context = {
    'form': form
  }
  return render_template('register.html', **context)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('login'))

# /profile/
@app.route('/profile/<name>', methods=['GET', 'POST'])
def profile(name):
  form = BlogForm()
  if form.validate_on_submit():
    p = Post(body=form.body.data, user_id=current_user.id)
    db.session.add(p)
    db.session.commit()
    flash("Post added successfully", 'success')
    return redirect(url_for('profile'))
  context = {
    'form': form,
    'posts': Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc()).all()
  }
  return render_template('profile.html', **context)

@app.route('/post/delete/<int:id>')
def post_delete(id):
  p = Post.query.get(id)
  db.session.delete(p)
  db.session.commit()
  flash("Post deleted successfully", "info")
  return redirect(url_for('profile', id=current_user.id))

@app.route('/users')
def users():
  context = {
    'users': User.query.all(),
    'following': current_user.followed.all()
  }
  return render_template('users.html', **context)

@app.route('/users/add/<user>')
def users_add(user):
  user = User.query.filter_by(name=user).first()
  print(user.name)
  print(current_user.followed)
  if user not in current_user.followed:
    flash("User added successfully", "success")
    current_user.follow(user)
    return redirect(url_for('users'))
  flash(f"You are already following {user.name}.", "warning")
  return redirect(url_for('users'))

@app.route('/users/remove/<user>')
def users_remove(user):
  user = User.query.filter_by(name=user).first()
  if user in current_user.followed:
    flash("User removed successfully", "success")
    current_user.unfollow(user)
    return redirect(url_for('users'))
  flash(f"You cannot unfollow someone you're not following. Make it make sense, sis...", "warning")
  return redirect(url_for('users'))