from app import db
from app.blueprints.main import main
from flask import render_template, redirect, url_for, request, flash
from app.blueprints.main.forms import BlogForm, ContactForm
from app.blueprints.account.forms import ProfileForm
from flask_login import login_required, current_user
from app.models import Post
from app.email import send_email

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
  form = BlogForm()
  context = {
    'form': form,
    'posts': current_user.followed_posts()
  }
  if form.validate_on_submit():
    p = Post(body=form.body.data, user_id=current_user.id)
    db.session.add(p)
    db.session.commit()
    flash("Post added successfully", 'success')
    return redirect(url_for('main.index'))
  return render_template('main/index.html', **context)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
  context = {
    'form': form
  }
  if form.validate_on_submit():
    send_email()
    flash("Your form submission was successful", "info")
    return redirect(url_for('main.contact'))
  return render_template('main/contact.html', **context)

@main.route('/about', methods=['GET', 'POST'])
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
    return redirect(url_for('main.about'))
  return render_template('main/about.html', **context)

@main.route('/post/delete/<int:id>')
@login_required
def post_delete(id):
  p = Post.query.get(id)
  db.session.delete(p)
  db.session.commit()
  flash("Post deleted successfully", "info")
  return redirect(url_for('account.profile', name=current_user.name.lower()))