# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# message = Mail(
#     from_email='sunkunxi@gmail.com',
#     to_emails='diboxjelly@gmail.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     sg = SendGridAPIClient("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")
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e.message)