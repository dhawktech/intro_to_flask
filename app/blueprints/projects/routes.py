from flask import render_template, redirect, url_for, flash, session
from app.blueprints.projects import projects
from flask_login import login_required
from app.blueprints.projects.forms import AutomationForm
from app.blueprints.projects.connection import connection, populate_form_from_database
import math, statistics, mysql.connector, os
from app.blueprints.projects.stripe import stripe, products, convert_price, getUSD
from decimal import Decimal

@projects.route('/automation', methods=['GET', 'POST'])
@login_required
def automation():
  form = AutomationForm()
  session['database'] = form.database.data
  form.database.data = session['database']
  if form.database.data is None:
    # print("form.database.data is:", "Unefined")
    conn = connection()
    populate_form_from_database(conn, 'databases', form.database)
    session['databases_choices'] = form.database.choices
    context = {
      'form': form,
      'label': 'Search Database',
    }
    return render_template('projects/automation.html', **context)
  else:
    # print("form.database.data is:", "Defined")
    form.database.data = session['database'] # set database choice to last selected database from previous redirect
    conn = connection(session['databases_choices'][form.database.data][1].lower())
    populate_form_from_database(conn, 'databases', form.database)
    populate_form_from_database(conn, 'tables', form.table)
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
  try:
    if session['cart']:
      pass
  except:
    session['cart'] = list()
  context = {
    'products': products
  }
  return render_template('projects/ecommerce.html', **context)

@projects.route('/ecommerce/cart')
@login_required
def ecommerceCart():
  try:
    cart = []
    for i in session['cart']:
      if i not in cart:
        cart.append(i)
  except:
    session['cart'] = list()
  context = {
    'cart': cart,
    'trueCart': session['cart'],
    'convert_price': convert_price,
    'grandTotal': getUSD(convert_price(getUSD(sum([i['price'] for i in session['cart']]))) + convert_price(getUSD(sum([i['price'] for i in session['cart']]))))
  }
  return render_template('projects/ecommerce_cart.html', **context)

@projects.route('/ecommerce/cart/add/product/<product>')
@login_required
def ecommerceCartAdd(product):
  product = stripe.SKU.retrieve(product)
  session['cart'].append(product)
  flash("Item added to cart.", "info")
  return redirect(url_for('projects.ecommerce'))

@projects.route('/ecommerce/cart/clear')
@login_required
def ecommerceCartClear():
  if len(session['cart']) > 0:
    session['cart'] = list()
    flash("All items removed from your cart.", "warning")
  else:
    flash("You currently have no items in your cart to begin with.", "info")
  return redirect(url_for('projects.ecommerceCart'))

@projects.route('/databases')
@login_required
def databases():
  context = {
  }
  return render_template('projects/databases.html', **context)

