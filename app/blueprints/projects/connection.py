import mysql.connector, os

def connection(db_name=None):
  return mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    passwd=os.environ.get('MYSQL_PSWD'),
    db=db_name,
    port=os.environ.get('MYSQL_PORT')
  )

def get_from_database(db, item, form):
  cur = db.cursor()
  cur.execute(f'SHOW {item}')
  choices = cur.fetchall()
  form.database.choices.extend(list(zip(list([i[0].decode('utf-8') for i in choices].index(i)+1 for i in [i[0].decode('utf-8') for i in choices]), [i[0].decode('utf-8').title() for i in choices])))
  cur.close()