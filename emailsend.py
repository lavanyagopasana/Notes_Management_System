import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDER_EMAIL = "lavanyagopasana@gmail.com"  # must match verified sender

def emailSend(to_email: str, subject: str, body: str):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response)
        print("SendGrid status code:", response.status_code)
        return "Email sent successfully" if response.status_code in [200, 202] else response.body
    except Exception as e:
        print("SendGrid error:", e)
        return f"Email failed: {e}"
