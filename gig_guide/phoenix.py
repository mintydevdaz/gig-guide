import itertools
import re
from datetime import datetime

import bs4
import requests
from bs4 import BeautifulSoup


def main():
    # Request HTML
    main_page = "https://phoenixcentralpark.com.au/season-vii"
    response = get_response(url=main_page)

    # Parse HTML
    soup = parse(r=response)

    # Extract individual event URLs
    urls = get_urls(soup)

    # Extract event details
    dates = []
    events = []
    for url in urls:
        # Get HTML & parse
        response = get_response(url)
        soup = parse(response)
        # Get headline act & date. Append to lists.
        d = event_date(soup)
        e = event_name(soup)
        dates.append(d)
        events.append(e)

    # Convert dates to datetime objects
    dt = convert_to_dt(dates)
    # Format dates (dd-mmm-yyyy) and weekday
    str_dates = string_dates(dt)
    str_days = string_weekdays(dt)

    # Generate list with venue name
    venue_list = list(itertools.repeat("Phoenix Central Park", len(urls)))

    # Create table
    table = prepare_table(
        datetime_objects=dt,
        str_dates=str_dates,
        weekday=str_days,
        events=events,
        venue=venue_list,
        urls=urls,
    )

    print(*table, sep="\n")


def get_response(url):
    """Get HTML response"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        return r
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def parse(r: requests.models.Response) -> bs4.BeautifulSoup:
    """Parse HTML"""
    return BeautifulSoup(r.text, features="lxml")


def get_urls(soup: bs4.BeautifulSoup) -> list[str]:
    """Obtain event URLs from webpage"""
    links = [link["href"] for link in soup.findAll("a", href=True)]
    return list({url for url in links if "https://phoenixcentralpark.com.au" in url})


def event_date(soup: bs4.BeautifulSoup) -> str:
    """Obtain date and time of event"""
    extract = soup.findAll("p", class_="sqsrte-large")
    date = extract[-1].text if len(extract) != 1 else extract[0].text
    d = re.split("(2023)", date)
    text = f"{d[0]}{d[1]}"
    return text[4:]


def event_name(soup: bs4.BeautifulSoup) -> str:
    """Extracts name of event"""
    return soup.find("h1").text


def convert_to_dt(dates: list[str]) -> list[datetime]:
    """Parse dates into datetime objects"""
    dt_objects = []
    for d in dates:
        i = datetime.strptime(d, "%d %B %Y")
        dt_objects.append(i)
    return dt_objects


def string_dates(dt: list[datetime]) -> list[str]:
    """Format datetime objects into dd-mmm-yyyy format"""
    str_dates = []
    for d in dt:
        i = d.strftime("%d-%b-%-y")
        str_dates.append(i)
    return str_dates


def string_weekdays(dt: list[datetime]) -> list[str]:
    """Format datetime objects into weekday"""
    str_days = []
    for day in dt:
        i = day.strftime("%a")
        str_days.append(i)
    return str_days


def prepare_table(
    datetime_objects: list[datetime],
    str_dates: list[str],
    weekday: list[str],
    events: list[str],
    venue: list[str],
    urls: list[str],
) -> list:
    return list(zip(datetime_objects, str_dates, weekday, events, venue, urls))


if __name__ == "__main__":
    main()
