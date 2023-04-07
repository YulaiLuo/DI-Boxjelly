from flask_restful import Resource
from flask import render_template
from flask_mail import Message

class Mail(Resource):

    def __init__(self, mail):
        self.mail = mail

    def post(self):
        msg = Message("Hello",
                      sender="", # Replace with your email address
                        recipients=["
                        "]) # Replace with your email address
        msg.body = "This is the email body"
        self.mail.send(msg)
        
        return None        

    # def send(self, to, subject, template, **kwargs):
    #     """
    #     Send an email to the given recipient.
    #     """
    #     msg = Message(subject, recipients=[to])
    #     msg.body = render_template(template + '.txt', **kwargs)
    #     msg.html = render_template(template + '.html', **kwargs)
    #     self.mail.send(msg)