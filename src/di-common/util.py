from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(to_emails,subject,html_content):
    # You need to add a sender email address to your SendGrid account
    # I add sunkunxi@qq.com here for example
    message = Mail(
        from_email='sunkunxi@qq.com',
        to_emails=to_emails,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e)

