from flask import cli, current_app
import os, click

@current_app.cli.group()
def blueprint():
  """Flask Blueprint commands"""
  pass

@blueprint.command()
@click.argument('name')
def create(name):
  """Create new Flask Blueprint"""
  basepath = os.path.abspath(os.path.dirname(__name__)) + f'/app/blueprints/{name}'
  try:
    if not os.path.exists(basepath):
      os.makedirs(basepath)
      init_file = open(f'{basepath}/__init__.py', 'w')
      init_file.close()
      routes_file = open(f'{basepath}/routes.py', 'w')
      routes_file.close()
      forms_py = open(f'{basepath}/forms.py', 'w')
      forms_py.close()
      os.makedirs(basepath + '/static')
      os.makedirs(basepath + '/static/css')
      css_file = open(f'/{basepath}/static/css/{name}.css', 'w')
      css_file.close()
      os.makedirs(basepath + '/static/js')
      os.makedirs(f'{basepath}/templates/{name}')
  except error:
    print(f"Something went wrong with creating the blueprint called {name}")
    print(error)
  return print("Blueprint created successfully")