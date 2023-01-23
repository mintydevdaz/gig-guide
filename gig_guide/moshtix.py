import itertools
import sys
from datetime import datetime

import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from database import moshtix_links


def main():
    print('Retrieving Moshtix event information')
    data = {"DT": [], "Date": [], "Event": [], "Venue": [], "URL": []}
    for venue, url in moshtix_links.items():

        # Get HTML response & parse
        r = get_html_response(url)
        soup = parse_html(response=r)

        # Retrieve event date, title, & url
        dates = event_dates(soup[0])
        events = event_title(soup[1])
        urls = event_urls(soup[1])

        # Parse date into datetime object. Re-format into string.
        dt = convert_datetime(dates)
        dt_dates = string_dates(dt)

        # Create venue list
        venues = list(itertools.repeat(venue, len(dates)))

        # Update Dictionary
        data["DT"] += dt
        data["Date"] += dt_dates
        data["Event"] += events
        data["Venue"] += venues
        data["URL"] += urls

    # Create DataFrame
    df = table(data)
    write_csv(df)


def get_html_response(url: str) -> requests.models.Response:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        sys.exit(f"HTTP error occurred: \n'{http_err}'")
    except requests.exceptions.Timeout as timeout_err:
        sys.exit(f"Timeout error occurred: \n'{timeout_err}'")
    except Exception as err:
        sys.exit(f"Error occurred: \n'{err}'")
    return r


def parse_html(response: requests.models.Response) -> tuple:
    """Extracts the raw dates and events from the website"""
    soup = BeautifulSoup(response.text, features="lxml")
    dates = soup.findAll("h2", class_="main-artist-event-header")
    events = soup.findAll("h2", class_="main-event-header")
    return dates, events


def event_dates(dates: bs4.element.ResultSet) -> list[str]:
    """Prepares dates for parsing into a datetime object"""
    # Get text from HTML
    pass_one = [date.text for date in dates]
    # Remove whitespace and line separators
    pass_two = [p.split() for p in pass_one]
    # List of cleaned dates
    pass_three = [" ".join(p[1:4]) for p in pass_two]
    return [i.replace(",", "") for i in pass_three]


def convert_datetime(dates: list[str]) -> list[datetime]:
    res = []
    for date in dates:
        i = datetime.strptime(date, "%d %b %Y")
        res.append(i)
    return res


def string_dates(dt_objects: list[datetime]) -> list[str]:
    """Format datetime objects into dd-mmm-yy format"""
    res = []
    for dt in dt_objects:
        i = dt.strftime("%d-%b-%-y (%a)")
        res.append(i)
    return res


def event_title(events: bs4.element.ResultSet) -> list[str]:
    # Get text from HTML
    pass_one = [e.text for e in events]
    # Remove whitespace and line separators
    pass_two = [p.split() for p in pass_one]
    # List of bands
    return [" ".join(p) for p in pass_two]


def event_urls(events: bs4.element.ResultSet) -> list[str]:
    urls = []
    for event in events:
        urls.extend(e["href"] for e in event.findAll("a"))
    return urls


def table(dict_data: dict) -> pd.DataFrame:
    return pd.DataFrame(dict_data)


# !! DELETE
def write_csv(df):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    filepath = f"/Users/darrenchung/Desktop/moshtix-gigs_{dt_string}.csv"
    print(f"CSV file saved at {filepath}")
    return df.to_csv(filepath, index=False)


if __name__ == "__main__":
    main()
