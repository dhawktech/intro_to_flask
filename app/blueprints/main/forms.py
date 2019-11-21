from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class BlogForm(FlaskForm):
  body = StringField(validators=[DataRequired()])
  submit = SubmitField(label="Submit")
  
class ContactForm(FlaskForm):
  name = StringField(validators=[DataRequired()])
  email = StringField(validators=[DataRequired(), Email()])
  message = TextAreaField(validators=[DataRequired()])
  submit = SubmitField(label="Submit")