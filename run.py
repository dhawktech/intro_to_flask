from app import app, db
from app.models import User

@app.shell_context_processor
def make_shell_context():
  return dict(
    app=app,
    db=db,
    User=User
  )