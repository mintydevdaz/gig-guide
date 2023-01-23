import itertools
import re
import sys
from datetime import datetime

import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from database import phoenix_link


def main():
    # Get HTML response & parse. Extract invidiual event URLs.
    link = phoenix_link.get("Phoenix Central Park")
    r = get_html_response(url=link)
    soup = parse_html(response=r)
    urls = get_urls(soup)

    # Cycle through each url
    dates = []
    events = []
    for url in urls:

        # Get HTML response & parse
        r = get_html_response(url)
        soup = parse_html(response=r)

        # Get headline act & date
        d = event_date(soup)
        e = event_name(soup)
        dates.append(d)
        events.append(e)

    # Parse date into datetime object. Re-format into string.
    dt = convert_datetime(dates)
    dt_dates = string_dates(dt)

    # Generate list with venue name
    venues = list(itertools.repeat("Phoenix Central Park", len(dates)))

    # Intialise & update dictionary
    data = {"DT": [], "Date": [], "Event": [], "Venue": [], "URL": []}
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


def parse_html(response: requests.models.Response) -> bs4.BeautifulSoup:
    return BeautifulSoup(response.text, features="lxml")


def get_urls(soup: bs4.BeautifulSoup) -> list[str]:
    links = [link["href"] for link in soup.findAll("a", href=True)]
    return list({url for url in links if "https://phoenixcentralpark.com.au" in url})


def event_date(soup: bs4.BeautifulSoup) -> str:
    extract = soup.findAll("p", class_="sqsrte-large")
    date = extract[-1].text if len(extract) != 1 else extract[0].text
    d = re.split("(2023)", date)
    text = f"{d[0]}{d[1]}"
    return text[4:]


def event_name(soup: bs4.BeautifulSoup) -> str:
    return soup.find("h1").text


def convert_datetime(dates: list[str]) -> list[datetime]:
    dt_objects = []
    for d in dates:
        i = datetime.strptime(d, "%d %B %Y")
        dt_objects.append(i)
    return dt_objects


def string_dates(dt: list[datetime]) -> list[str]:
    """Format datetime objects into dd-mmm-yy format"""
    str_dates = []
    for d in dt:
        i = d.strftime("%d-%b-%-y (%a)")
        str_dates.append(i)
    return str_dates


def table(dict_data: dict) -> pd.DataFrame:
    return pd.DataFrame(dict_data)


# !! DELETE
def write_csv(df):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    filepath = f"/Users/darrenchung/Desktop/phoenix-gigs_{dt_string}.csv"
    print(f"CSV file saved at {filepath}")
    return df.to_csv(filepath, index=False)


if __name__ == "__main__":
    main()
