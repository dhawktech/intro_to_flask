from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class ProfileForm(FlaskForm):
  name = StringField(validators=[DataRequired()])
  email = StringField(validators=[DataRequired(), Email()])
  password = PasswordField(validators=[DataRequired(), EqualTo('confirm_password')])
  confirm_password = PasswordField(validators=[DataRequired()])
  submit = SubmitField(label="Submit")

class RegistrationForm(FlaskForm):
  name = StringField(validators=[DataRequired()])
  email = StringField(validators=[DataRequired(), Email()])
  password = PasswordField(validators=[DataRequired(), EqualTo('confirm_password')])
  confirm_password = PasswordField(validators=[DataRequired()])
  submit = SubmitField(label="Submit")

class LoginForm(FlaskForm):
  email = StringField(validators=[DataRequired()])
  password = PasswordField(validators=[DataRequired()])
  remember_me = BooleanField()
  submit = SubmitField(label="Login")