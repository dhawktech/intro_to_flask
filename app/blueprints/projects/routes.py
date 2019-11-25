from flask import render_template, redirect, url_for, flash, session
from app.blueprints.projects import projects
from flask_login import login_required
from app.blueprints.projects.forms import AutomationForm
from app.blueprints.projects.connection import connection
import math, statistics, mysql.connector, os

@projects.route('/automation', methods=['GET', 'POST'])
@login_required
def automation():
  form = AutomationForm()
  session['database'] = form.database.data
  form.database.data = session['database']
  if form.database.data is None:
    # print("form.database.data is:", "Unefined")
    conn = connection()
    cur = conn.cursor()
    cur.execute('SHOW DATABASES')
    choices = cur.fetchall()
    form.database.choices.extend(list(zip(list([i[0].decode('utf-8') for i in choices].index(i)+1 for i in [i[0].decode('utf-8') for i in choices]), [i[0].decode('utf-8').title() for i in choices])))
    session['databases_choices'] = form.database.choices
    cur.close()
    context = {
      'form': form,
      'label': 'Search Database',
    }
    return render_template('projects/automation.html', **context)
  else:
    # print("form.database.data is:", "Defined")
    form.database.data = session['database'] # set database choice to last selected database from previous redirect
    conn = connection(session['databases_choices'][form.database.data][1].lower())
    cur = conn.cursor()
    cur.execute('SHOW DATABASES')
    choices = cur.fetchall()
    form.database.choices.extend(list(zip(list([i[0].decode('utf-8') for i in choices].index(i)+1 for i in [i[0].decode('utf-8') for i in choices]), [i[0].decode('utf-8').title() for i in choices])))
    cur.close()
    cur = conn.cursor()
    cur.execute('SHOW TABLES')
    choices = cur.fetchall()
    form.table.choices.extend(list(zip(list([i[0].decode('utf-8') for i in choices].index(i)+1 for i in [i[0].decode('utf-8') for i in choices]), [i[0].decode('utf-8').title() for i in choices])))
    cur.close()
    if form.validate_on_submit():
      if not form.table.choices:
        flash("Must select a valid option. Try again", "warning")
      cur = conn.cursor()
      cur.execute(f"SELECT * FROM {form.table.choices[form.table.data][1].lower()}")
      data = cur.fetchall()
      context = {
        'form': form,
        'data': dict(
                  rows=data,
                  columns=cur.column_names,
                ),
        'is_database': True,
        'is_table': True,
        'label': 'Search Table'
      }
      cur.close()
      conn.close()
      flash("Successful database query", "success")
      return render_template('projects/automation.html', **context)
    context = {
      'form': form,
      'is_database': True,
      'label': 'Search Table',
    }
    return render_template('projects/automation.html', **context)

@projects.route('/ecommerce')
@login_required
def ecommerce():
  context = {}
  return render_template('projects/ecommerce.html', **context)

@projects.route('/databases')
@login_required
def databases():
  context = {}
  return render_template('projects/databases.html', **context)

