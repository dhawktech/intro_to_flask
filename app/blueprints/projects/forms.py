from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class AutomationForm(FlaskForm):
  database = SelectField(validators=[DataRequired()], choices=[(0, '-- Select a Database --')], coerce=int)
  table = SelectField(validators=[DataRequired()], choices=[(0, '-- Select a Table --')], coerce=int)
  submit = SubmitField()