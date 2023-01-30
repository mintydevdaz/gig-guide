import os
import smtplib
from pathlib import Path

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

    # Get Desktop path. Prepare file attachment.
    parent_dir = str(Path.home() / "Desktop")
    path = f"{parent_dir}/gigs_email.csv"
    content = attachment(path)

    # Login to Gmail Account
    SERVER_ADDRESS = "smtp.gmail.com"
    TLS_PORT = 587
    with smtplib.SMTP(SERVER_ADDRESS, TLS_PORT) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)

        # Cycle through list of receiving email addresses
        for name, receiver in receivers.items():

            # Prepare email body (plain text & html)
            plain_text = body(name)
            html_body = get_html_body(name, html_table)

            # Instantiate email
            msg = create_email_message(
                from_address=SENDER,
                to_address=receiver,
                body=plain_text,
                html_body=html_body,
                attachment=content,
                csv_path="gigs.csv",
            )
            server.send_message(msg)
            print(f"-> Email sent to {name} ({receiver})")

    # Delete Master CSV & gigs_email CSV
    os.remove(f"{parent_dir}/gigs_master.csv")
    os.remove(path)
    print(f"Removed files from {parent_dir}")


if __name__ == "__main__":
    main()
