import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = "your_verified_sender_email@example.com"  # must be verified in SendGrid

def emailSend(to_email: str, subject: str, body: str):
    try:
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=to_email,
            subject=subject,
            plain_text_content=body
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return f"Email sent successfully! Status code: {response.status_code}"
    except Exception as e:
        return f"Error sending email: {e}"
