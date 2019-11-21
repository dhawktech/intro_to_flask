from flask import current_app

@current_app.context_processor
def getGlobal():
  return dict(
    g_username=""
  )
