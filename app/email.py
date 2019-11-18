from flask_mail import Message
from app import mail

def send_mail(subject, sender, recipients, body):
  msg = Message(subject, recipients=recipients, sender=sender)
  body = render_template('email/email.html')
  msg.html = body
  mail.send(msg)