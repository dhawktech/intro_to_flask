from flask import Blueprint

apis = Blueprint('apis', __name__, template_folder='templates', static_folder='static')

from app.blueprints.apis import routes