import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import generate


def send_email(to_email, subject, body_text, gmail_user, app_password):
    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach the email body
    msg.attach(MIMEText(body_text, "plain"))

    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(gmail_user, app_password)  # Login with your Gmail account

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()  # Disconnect from the server
