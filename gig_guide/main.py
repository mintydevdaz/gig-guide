import os

from compile_data import body_table, email_file, master_file
from dotenv import load_dotenv
from message import message


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

    # Send email
    message(
        html_table=html_table,
        csv_file="/Users/darrenchung/Desktop/gigs_email.csv",
        user_email=SENDER,
        user_password=PASSWORD
    )


if __name__ == "__main__":
    main()
