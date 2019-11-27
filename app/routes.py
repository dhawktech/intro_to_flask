from flask import current_app, session

@current_app.context_processor
def getGlobal():
  return dict(
    cart=session['cart']
  )
