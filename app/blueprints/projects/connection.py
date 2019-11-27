import mysql.connector, os

def connection(db_name=None):
  return mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    passwd=os.environ.get('MYSQL_PSWD'),
    db=db_name,
    port=os.environ.get('MYSQL_PORT')
  )

def populate_form_from_database(db, strObj, formDbObj):
  cur = db.cursor()
  cur.execute(f'SHOW {strObj.upper()}')
  choices = cur.fetchall()
  formDbObj.choices.extend(list(zip(list([i[0].decode('utf-8') for i in choices].index(i)+1 for i in [i[0].decode('utf-8') for i in choices]), [i[0].decode('utf-8').title() for i in choices])))
  cur.close()