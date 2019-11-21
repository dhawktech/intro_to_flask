from flask import Blueprint, render_template, redirect, url_for
import requests
from app.blueprints.apis.forms import ErgastForm, WeatherForm
from flask_login import login_required
import os, math

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

@bp.route('/weather', methods=['GET', 'POST'])
@login_required
def weather():
  form = WeatherForm()
  response = None
  data = None
  unit = None
  if form.validate_on_submit():
    print(form.units.data)
    if form.units.data == 0:
      unit = "°F"
    elif form.units.data == 1:
      unit = "°C"
    else:
      unit = "K"
    try:
      response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={form.city.data},{form.country.data}&appid={os.environ.get("OPENWEATHERMAP_API_KEY")}&units={dict(form.units.choices).get(form.units.data)}')
      data = response.json()
      context = {
        'data': dict(
          name=data['name'],
          country=data['sys']['country'],
          current=math.floor(data['main']['temp']),
          condition=data['weather'][0]['main'],
          clouds=data['clouds']['all'],
          high_temp=math.floor(data['main']['temp_max']),
          low_temp=math.floor(data['main']['temp_min']),
          unit=unit
        ),
        'form': form,
      }
      return render_template('apis/openweathermap.html', **context)
    except IndexError:
      context = {
        'data': data,
        'form': form,
        'message': 'There are no results for that year or season'
      }
      return render_template('apis/openweathermap.html', **context)
    except Exception as e:
      context = {
        'data': data,
        'form': form,
        'message': 'That is an invalid entry'
      }
      print('Error', e)
      return render_template('apis/openweathermap.html', **context)
  context = {
    'form': form,
    'data': data,
    'message': 'Search for something...'
  }
  return render_template('apis/openweathermap.html', **context)

