import smtplib
from email.mime.text import MIMEText
import os

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DOMAIN = os.getenv("DOMAIN")
    
def send_verification_email(to_email: str, to_user: str, verification_token: str):
    subject = "Verify Your Email Address"
    body = f"""
    Hi {to_user},

    Thank you for registering with us! Please click the link below to verify your email address:

    http://{DOMAIN}/api/user/verify?token={verification_token}

    If you did not register, please ignore this email.

    Best regards,
    Unimanager App Team
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string()) 