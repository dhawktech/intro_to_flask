from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

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

class ProfileForm(FlaskForm):
  name = StringField(validators=[DataRequired()])
  email = StringField(validators=[DataRequired(), Email()])
  password = PasswordField(validators=[DataRequired(), EqualTo('confirm_password')])
  confirm_password = PasswordField(validators=[DataRequired()])
  submit = SubmitField(label="Submit")

class BlogForm(FlaskForm):
  body = StringField(validators=[DataRequired()])
  submit = SubmitField(label="Submit")
  
class ContactForm(FlaskForm):
  name = StringField(validators=[DataRequired()])
  email = StringField(validators=[DataRequired(), Email()])
  message = TextAreaField(validators=[DataRequired()])
  submit = SubmitField(label="Submit")