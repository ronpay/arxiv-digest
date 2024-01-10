import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger('arxivdigest')

class email_pusher():
    def __init__(self):
        load_dotenv()
        self.email = os.getenv('GMAIL_ADDRESS')
        self.password = os.getenv('GMAIL_PASSWORD')
        self.to_email = os.getenv('TO_EMAIL_ADDRESS', self.email)

    def send_email(self, subject: str, body: str):
        logger.info(f'Sending email to {self.to_email}')
        logger.info(f'Email subject: {subject}')
        logger.info(f'Email body: {body}')
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = self.to_email
        msg.set_content(body)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.email, self.password)
            logger.info(f'login successful')
            smtp.send_message(msg)
            logger.info(f'email sent')