# importing required modules
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# load credentials from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
PASSKEY = os.getenv("EMAIL_PASSKEY")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

def emailSend(to_email: str, subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # server connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, PASSKEY)
        server.sendmail(from_addr=SENDER_EMAIL, to_addrs=to_email, msg=msg.as_string())
        server.quit()
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        # Instead of crashing, log the error
        print(f"Failed to send email to {to_email}: {e}")
        # Optionally return False to let the app know
        return False
    return True
