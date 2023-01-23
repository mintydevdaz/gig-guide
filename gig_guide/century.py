import sys
from datetime import datetime

import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from database import century_links


def century():
    dates = []
    events = []
    venues = []
    urls = []

    for venue, url in century_links.items():
        print(f'Retrieving {venue} event info')

        # Get HTML response & parse. Access HTML IDs.
        r = get_html_response(url)
        soup = parse_html(response=r)
        ids = get_html_ids(soup)

        for i in ids:

            # Get HTML response & parse. Access unique event page.
            sub_url = get_link(url, html_id=i)
            req = get_html_response(sub_url)
            soup_cup = parse_html(req)

            # Get event date, title, venue & url
            dates.append(event_date(soup_cup))
            events.append(event_title(soup_cup))
            venues.append(venue)
            urls.append(sub_url)

    # Parse date into datetime object. Re-format into string.
    dt = convert_datetime(dates)
    dt_dates = string_dates(dt)

    # Intialise & update dictionary
    data = {
        "DT": dt,
        "Date": dt_dates,
        "Event": events,
        "Venue": venues,
        "URL": urls
    }

    return table(data)


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


def parse_html(response: requests.models.Response) -> bs4.element.ResultSet:
    return BeautifulSoup(response.text, features="lxml")


def get_html_ids(soup: bs4.element.ResultSet) -> list[str]:
    """Get unique HTML ids"""
    return [tag["id"] for tag in soup.select("a[id]")]


def get_link(url: str, html_id: str) -> str:
    link = url.removesuffix("?s&key=upcoming")
    return f"{link}event/{html_id}/"


def event_date(soup: bs4.element.ResultSet) -> str:
    return soup.find("li", class_="session-date").text


def event_title(soup: bs4.element.ResultSet) -> str:
    return soup.find("h1", class_="title").text


def convert_datetime(dates: list[str]) -> list[datetime]:
    res = []
    for d in dates:
        i = datetime.strptime(d, "%A, %d %B %Y %I:%M %p")
        res.append(i)
    return res


def string_dates(dt_objects: list[datetime]) -> list[str]:
    """Format datetime objects into dd-mmm-yy format"""
    res = []
    for dt in dt_objects:
        i = dt.strftime("%d-%b-%-y (%a)")
        res.append(i)
    return res


def table(dict_data: dict) -> pd.DataFrame:
    return pd.DataFrame(dict_data)


if __name__ == "__main__":
    century()

