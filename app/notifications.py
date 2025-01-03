import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(subject: str, body: str, to_email: str):
    """
    Send an email notification.

    Args:
        subject (str): Subject of the email.
        body (str): Body of the email.
        to_email (str): Recipient's email address.
    """
    # Replace with your email credentials
    sender_email = os.getenv("MAIL_APP_EMAIL")
    sender_password = os.getenv("MAIL_APP_PASSWORD")

    # Configure the email message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":

    subject = "Price Drop Alert!"
    body = "The price of the product you are tracking has dropped. Check it out now!"
    to_email = "manavg@umd.edu"
    send_email(subject, body, to_email)
