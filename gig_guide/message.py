import smtplib
import ssl
from email.message import EmailMessage


# TODO: message takes in the CSV filepath and pretty_html_table

def message():
    # Sender / receiver information
    sender = "mintydevdaz@gmail.com"
    password = "ykipedwpyitqwsco"
    receiver = "darrenchung88@outlook.com"

    # Content of email
    subject = "Test Email"
    body = """
    Let the record show that is this is a test email.
    """

    # Instantiate EmailMessage class
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    # Create secure SSL connection
    context = ssl.create_default_context()

    # Login & send email
    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())


if __name__ == "__main__":
    message()
