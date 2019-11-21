from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ErgastForm(FlaskForm):
  year = StringField(validators=[DataRequired()])
  season = StringField(validators=[DataRequired()])
  # temp = SelectField(coerce=int, choices=[(0, '-- select an option --'), (1, 'Fahrenheit'), (2, 'Celsius'), (3, 'Kelvin')], default=0)
  submit = SubmitField('Submit')