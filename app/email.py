import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.forms import ContactForm
from flask import render_template

def send_email():
  form = ContactForm()
  context = {
    'recipient_name': 'Derek Hawkins',
    'sender_name': form.name.data,
    'message': form.message.data,
    'sender_email': form.email.data
  }
  message = Mail(
    from_email='noreply@codingtemple.com',
    to_emails='derek@codingtemple.com',
    subject='Contact Form Inquiry',
    html_content=render_template('email/email.html', **context)
  )
  try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
  except Exception as e:
    print(e.message)