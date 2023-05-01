from datetime import datetime


class Email:

    def __init__(self, sender, receivers, subject, content):
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
        self.content = content
        self.send_time = datetime.utcnow()
        self.status = 0 # 0: not sent, 1: sent, 2: failed

    def send(self):
        pass

