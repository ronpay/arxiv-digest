import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import logging

class email_pusher():
    def __init__(self):
        load_dotenv()
        self.email = os.getenv('GMAIL_ADDRESS')
        self.password = os.getenv('GMAIL_PASSWORD')
        self.to_email = os.getenv('TO_EMAIL', self.email)

    def send_email(self, subject: str, body: str):
        logging.info(f'Sending email to {self.to_email}')
        logging.info(f'Email subject: {subject}')
        logging.info(f'Email body: {body}')
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = self.to_email
        msg.set_content(body)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.email, self.password)
            logging.info(f'login successful')
            smtp.send_message(msg)
            logging.info(f'email sent')