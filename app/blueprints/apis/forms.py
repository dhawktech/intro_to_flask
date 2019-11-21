from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ErgastForm(FlaskForm):
  year = StringField(validators=[DataRequired()])
  season = StringField(validators=[DataRequired()])
  submit = SubmitField('Submit')

class WeatherForm(FlaskForm):
  city = StringField(validators=[DataRequired()])
  country = StringField(validators=[DataRequired()])
  units = SelectField(coerce=int, choices=[(0, 'Imperial'), (1, 'Metric'), (2, 'Kelvin')], default=0)
  submit = SubmitField('Submit')