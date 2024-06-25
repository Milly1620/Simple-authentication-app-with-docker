import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = os.getenv("SOURCE_EMAIL")
mail_user = os.getenv("MAIL_USERNAME")
sender_password = os.getenv("MAIL_PASSWORD")
smtp_server = os.getenv("MAIL_HOST")
smtp_port = os.getenv("MAIL_PORT")


def send_email(details, html_body):
    recipient = details['recipient_email']
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = details['subject']
    
    html_content = html_body.format(**details)
    part1 = MIMEText(html_content, "html")
    message.attach(part1)
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(mail_user, sender_password)
        server.sendmail(sender_email, recipient, message.as_string())

    return True

