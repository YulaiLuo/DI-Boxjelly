from flask_restful import Resource

class Mail(Resource):

    def __init__(self, mail):
        self.mail = mail

    def send(self, to, subject, template, **kwargs):
        """
        Send an email to the given recipient.
        """
        msg = Message(subject, recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        self.mail.send(msg)