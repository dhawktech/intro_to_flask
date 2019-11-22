from flask import render_template, redirect, url_for
from app.blueprints.projects import projects

@projects.route('/automation')
def automation():
  context = {}
  return render_template('projects/automation.html', **context)

@projects.route('/ecommerce')
def ecommerce():
  context = {}
  return render_template('projects/ecommerce.html', **context)

@projects.route('/databases')
def databases():
  context = {}
  return render_template('projects/databases.html', **context)

