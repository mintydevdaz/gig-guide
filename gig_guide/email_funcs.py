def attachment(csv_file: str) -> bytes:
    """Prepare CSV attachment for email(s)"""
    with open(csv_file, 'rb') as content_file:
        return content_file.read()


def body(name: str) -> str:
    """Returns email body in plain text"""
    return f"""
            Dear {name},

            Attached is the current list of gigs for the following venues:

            - Big Top Luna Park
            - Enmore Theatre
            - Factory Theatre
            - Lansdowne Hotel
            - Lazybones Lounge
            - Manning Bar
            - Metro Theatre
            - Oxford Art Factory
            - Phoenix Central Park
            - Sydney Opera House
            - The Concourse
            - UNSW Roundhouse

            Kind regards,
            Darren "Cool D" Chung
            """


def get_html_body(name: str, html_table: str) -> str:
    return f"""\
            <!DOCTYPE html>
            <html>
                <body>
                    <p>Dear {name},</p>
                    <p>Attached is the current list of gigs for the next 30
                    days at the following venues:</p>
                    <ul>
                        <li>Big Top Luna Park</li>
                        <li>Enmore Theatre</li>
                        <li>Factory Theatre</li>
                        <li>Lansdowne Hotel</li>
                        <li>Lazybones Lounge</li>
                        <li>Manning Bar</li>
                        <li>Metro Theatre</li>
                        <li>Oxford Factory Theatre</li>
                        <li>Phoenix Central Park</li>
                        <li>Sydney Opera House</li>
                        <li>The Councourse</li>
                        <li>UNSW Roundhouse</li>
                    </ul>
                    {html_table}
                    <p>Kind regards,
                    <br>Darren "Cool D" Chung<p>
                </body>
            </html>
            """
