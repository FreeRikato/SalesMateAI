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


# Usage
if __name__ == "__main__":
    # Read the final email content
    with open("../backend/logs/final_email.txt", "r") as file:
        email_body = file.read()

    # Define email details
    recipient_email = (
        "vishwadharaniv2003@gmail.com"  # Replace with the prospect's email address
    )
    email_subject = "Your Personalized Offer"
    gmail_user = "aravinthan@student.tce.edu"  # Replace with your Gmail address
    app_password = "ldmz moxp xufj qtgd"  # Replace with your generated app password

    # Send the email
    send_email(recipient_email, email_subject, email_body, gmail_user, app_password)
