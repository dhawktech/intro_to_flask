from flask import Blueprint, render_template, redirect, url_for
import requests
from app.blueprints.apis.forms import ErgastForm
from flask_login import login_required

bp = Blueprint('apis', __name__, template_folder='templates', static_folder='static')

@bp.route('/ergast', methods=['GET', 'POST'])
@login_required
def ergast():
  form = ErgastForm()
  response = None
  data = None
  if form.validate_on_submit():
    try:
      response = requests.get(f'https://ergast.com/api/f1/{form.year.data}/{form.season.data}/driverStandings.json')
      data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
      context = {
        'data': data,
        'form': form
      }
      return render_template('apis/ergast.html', **context)
    except IndexError:
      context = {
        'data': data,
        'form': form,
        'message': 'There are no results for that year or season'
      }
      return render_template('apis/ergast.html', **context)
    except:
      context = {
        'data': data,
        'form': form,
        'message': 'That is an invalid entry'
      }
      return render_template('apis/ergast.html', **context)
  context = {
    'form': form,
    'data': data,
    'message': 'Search for something...'
  }
  return render_template('apis/ergast.html', **context)
