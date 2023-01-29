import os
import smtplib
from datetime import date, datetime
from email.message import EmailMessage

from dotenv import load_dotenv
from email_funcs import attachment, body, get_html_body
from email_list import receivers

# TODO: add in links to SydneyMusic, Ticketek, Ticketmaster


def message(html_table: str, csv_file: str):
    # Load environmental variables
    x = load_dotenv(dotenv_path=os.path.basename('gig_guide/.env'))
    SENDER = os.getenv('SENDER')
    PASSWORD = os.getenv('PASSWORD')

    # Prepare file attachment
    content = attachment(csv_file)

    # !! unique day (CONSIDER DELETION)
    day = today()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(user=SENDER, password=PASSWORD)

        # Send to each person in dict
        for name, receiver in receivers.items():

            # Prepare body in plain text and html version
            print(f"Preparing email for {name} ({receiver})")
            plain_text = body(name)
            html_body = get_html_body(name, html_table)

            # Instantiate email func
            msg = EmailMessage()
            msg["From"] = SENDER
            msg["To"] = receiver
            msg["Subject"] = "Upcoming Gigs"
            msg.set_content(plain_text)
            msg.add_alternative(html_body, subtype="html")
            msg.add_attachment(content,
                               maintype="application",
                               subtype="csv",
                               filename=f"gigs_{day}.csv")

            server.send_message(msg)
            print("-> Email Sent")


def today() -> str():
    return datetime.strftime(date.today(), "%d-%b-%-y")


if __name__ == "__main__":
    message()
