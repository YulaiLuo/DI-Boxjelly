from flask import Flask, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask-Mail configuration
mail_settings = {
    "MAIL_SERVER": 'smtp.sendgrid.net',
    "MAIL_PORT": 465,
    # "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "apikey",
    "MAIL_PASSWORD": "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"
}

app.config.update(mail_settings)
mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    # to_email = request.form.get('to_email')
    # subject = request.form.get('subject')
    # content = request.form.get('content')
    to_email = "diboxjelly@gmail.com"
    subject = "Hello"
    content = "This is a test email I sent with Gmail and Python!"

    from_email = "sunkunxi@qq.com"  # Replace with your email address
    msg = Message(subject, sender=from_email, recipients=[to_email])
    msg.body = content
    mail.send(msg)

    return 'Email sent successfully', 200

if __name__ == '__main__':
    app.run(debug=True)