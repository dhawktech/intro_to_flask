from flask import render_template, redirect, url_for, flash, session
from app.blueprints.projects import projects
from flask_login import login_required
from app.blueprints.projects.forms import AutomationForm, ProductForm
from app.blueprints.projects.connection import connection, populate_form_from_database
import math, statistics, mysql.connector, os, stripe
from app.blueprints.projects.stripe import initProducts, convert_price

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
  productForm = ProductForm()
  productForm.quantity.choices.extend([(i, i) for i in range(1, 100)])
  try:
    if not session['cart']:
      initProducts()
      pass
  except:
    session['cart'] = list()
  if productForm.validate_on_submit():
    print('It works')
    flash("Item added to the cart")
    return redirect(url_for('projects.ecommerce'))
  context = {
    'products': initProducts(),
    'productForm': productForm
  }
  return render_template('projects/ecommerce.html', **context)

@projects.route('/ecommerce/cart')
@login_required
def ecommerceCart():
  try:
    shallowCart = []
    for i in session['cart']:
      if i not in shallowCart:
        shallowCart.append(i)
    for i in shallowCart:
      i['quantity'] = session['cart'].count(i)
  except:
    session['cart'] = list()
    initProducts()
  context = {
    'products': initProducts(),
    'cart': session['cart'],
    'shallowCart': shallowCart,
    'grandTotal': round(sum([i['price'] for i in session['cart']]), 2),
    'round': round
  }
  return render_template('projects/ecommerce-cart.html', **context)

@projects.route('/ecommerce/cart/add/product/<id>', methods=['GET', 'POST'])
@login_required
def ecommerceCartAdd(id):
  p = stripe.SKU.retrieve(id)
  product = dict(
    id=p.id,
    prod_id=p.product,
    name=p.attributes.name,
    image=p.image,
    price=convert_price(p.price)
  )
  session['cart'].append(product)
  flash(f"[{product['name']}] added to your shopping cart.", "info")
  return redirect(url_for('projects.ecommerce'))

@projects.route('/ecommerce/cart/clear')
@login_required
def ecommerceCartClear():
  if session['cart']:
    session['cart'] = list()
    flash("You have cleared all items from your cart.", "info")
  else:
    flash("You cannot clear items from a cart you don't have.", "warning")
  return redirect(url_for('projects.ecommerceCart'))

@projects.route('/ecommerce/cart/remove/<id>')
@login_required
def ecommerceCartRemove(id):
  product = stripe.SKU.retrieve(id)
  try:
    for i in session['cart']:
      if product['id'] == i['id']:
        session['cart'].remove(i)
        flash(f"You have removed {product.attributes.name}.", "info")
        break
  except:
    flash(f"{product.attributes.name} could not be removed", "warning")
  return redirect(url_for('projects.ecommerceCart'))

@projects.route('/ecommerce/cart/product/add/<product>', methods=['POST'])
@login_required
def ecommerceCartProductAdd(product):
  form = ProductForm()
  if form.submit():
    for i in initProducts():
      if product == i['name']:
        session['cart'].extend([i] * form.quantity.data)
        break
    flash(f"You've added {form.quantity.data} {product}(s) to your cart.", "info")
  return redirect(url_for('projects.ecommerce'))

@projects.route('/databases')
@login_required
def databases():
  context = {
  }
  return render_template('projects/databases.html', **context)