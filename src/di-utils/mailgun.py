from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.mailgun.org',
    "MAIL_PORT": 465,
    # "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "postmaster@sandbox6672c8f55a874ce0a9f4056b590587f7.mailgun.org",
    "MAIL_PASSWORD": "e2f34468cf0e54d7da65c6e9726584aa-30344472-3ca98978"
}

app.config.update(mail_settings)
mail = Mail(app)

if __name__ == '__main__':
    with app.app_context():
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["diboxjelly@gmail.com"], # replace with your email for testing
                      body="This is a test email I sent with Gmail and Python!")
        mail.send(msg)