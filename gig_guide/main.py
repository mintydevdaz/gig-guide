import os
import smtplib

from compile_data import body_table, email_file, master_file
from dotenv import load_dotenv
from email_funcs import attachment, body, create_email_message, get_html_body
from email_list import receivers


def main():
    # Create Master file (CSV)
    df = master_file()

    # Create email attachment (CSV)
    email_file(df)

    # Create HTML table
    html_table = body_table()

    # Get environment variables
    load_dotenv(dotenv_path=os.path.basename("gig_guide/.env"))
    SENDER = os.getenv("SENDER")
    PASSWORD = os.getenv("PASSWORD")

    # Prepare file attachment
    path = "/Users/darrenchung/Desktop/gigs_email.csv"
    content = attachment(path)

    # Login to Gmail Account
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)

        # Cycle through list of receiving email addresses
        for name, receiver in receivers.items():

            # Prepare email body in plain text & html
            print(f"Preparing email for {name} ({receiver})")
            plain_text = body(name)
            html_body = get_html_body(name, html_table)

            # Instantiate email
            msg = create_email_message(
                from_address=SENDER,
                to_address=receiver,
                body=plain_text,
                html_body=html_body,
                attachment=content,
                csv_path=path
            )
            server.send_message(msg)
            print("-> Email Sent")


if __name__ == "__main__":
    main()
