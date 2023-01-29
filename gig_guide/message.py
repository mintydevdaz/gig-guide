import smtplib

from email_funcs import attachment, body, create_email_message, get_html_body
from email_list import receivers


def message(
    html_table: str, csv_file: str, user_email: str, user_password: str
):

    # Prepare file attachment
    content = attachment(csv_file)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(user=user_email, password=user_password)

        # Send to each person in dict
        for name, receiver in receivers.items():

            # Prepare body in plain text and html version
            print(f"Preparing email for {name} ({receiver})")
            plain_text = body(name)
            html_body = get_html_body(name, html_table)

            # Instantiate email
            msg = create_email_message(
                from_address=user_email,
                to_address=receiver,
                body=plain_text,
                html_body=html_body,
                attachment=content,
                csv_path=csv_file
            )

            server.send_message(msg)
            print("-> Email Sent")


if __name__ == "__main__":
    message()
