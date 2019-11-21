from app import db
from flask import current_app, render_template

@current_app.errorhandler(404)
def not_found_error(error):
  return render_template('errors/errors.html', error=error), 404

@current_app.errorhandler(500)
def internal_error(error):
  db.session.rollback()
  return render_template('errors/errors.html', error=error), 500