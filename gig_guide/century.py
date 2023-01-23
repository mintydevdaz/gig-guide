from datetime import datetime
from operator import itemgetter

import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from database import century_links


def main():
    dates = []
    events = []
    venues = []
    links = []

    for venue, url in century_links.items():

        print(f"Retrieving data for {venue}")

        # Request HTML from venue's webpage
        request = get_html(url)
        soup = parse(request)
        ids = get_html_ids(soup)

        for i in ids:
            # Request HTML frim individual event webpage
            sub_url = get_new_url(url, i)
            sub_request = get_html(sub_url)
            soup_cup = parse(sub_request)

            # Get event's date
            date = event_date(soup_cup)
            dates.append(date)

            # Get event name
            event = event_name(soup_cup)
            events.append(event)

            # Get URL link
            links.append(sub_url)

            # Add venue
            venues.append(venue)

    # Convert dates to datetime objects
    dt = convert_to_dt(dates)
    # Format dates (dd-mmm-yyyy) and weekday
    str_dates = string_dates(dt)
    str_days = string_weekdays(dt)

    # Create table
    gigs = prepare_table(
        datetime_objects=dt,
        str_dates=str_dates,
        weekday=str_days,
        events=events,
        venues=venues,
        urls=links,
    )

    # Sort by datetime
    final_sort = sorted(gigs, key=itemgetter(0))

    # Construct table and remove first column
    df = table(final_sort)
    df2 = remove_col(df)

    # Save CSV file
    write_csv(df2)


def get_html(url: str) -> requests.models.Response:
    # Get request from URL
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }  # noqa
        r = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.HTTPError as err:
        print(err)
    except requests.exceptions.Timeout as err:
        print(err)
    return r


def parse(r: requests.models.Response) -> bs4.element.ResultSet:
    """Parse HTML"""
    return BeautifulSoup(r.text, features="lxml")


def get_html_ids(soup: bs4.element.ResultSet) -> list[str]:
    """Get unique HTML ids"""
    return [tag["id"] for tag in soup.select("a[id]")]


def get_new_url(url: str, html_id: str) -> str:
    link = url.removesuffix("?s&key=upcoming")
    return f"{link}event/{html_id}/"


def event_date(soup: bs4.element.ResultSet) -> str:
    return soup.find("li", class_="session-date").text


def event_name(soup: bs4.element.ResultSet) -> str:
    return soup.find("h1", class_="title").text


def convert_to_dt(dates: list[str]) -> list[datetime]:
    """Parse dates into datetime objects"""
    dt_objects = []
    for d in dates:
        i = datetime.strptime(d, "%A, %d %B %Y %I:%M %p")
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
    venues: list[str],
    urls: list[str],
) -> list:
    return list(zip(datetime_objects, str_dates, weekday, events, venues, urls))


def table(gigs: list) -> pd.DataFrame:
    """Table of gigs"""
    return pd.DataFrame(
        gigs, columns=["dt", "Date", "Weekday", "Event", "Venue", "Link"]
    )


def remove_col(df):
    return df.drop("dt", axis="columns")


def write_csv(df):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    filepath = f"/Users/darrenchung/Desktop/coolgigs_{dt_string}.csv"
    print(f"CSV file saved at {filepath}")
    return df.to_csv(filepath, index=False)


if __name__ == "__main__":
    main()
