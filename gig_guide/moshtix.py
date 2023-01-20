import itertools
from datetime import datetime
from operator import itemgetter

import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from moshtix_urls import links


def main():
    res = []
    for venue, url in links.items():

        # Requests HTML
        response = get_response(url)

        # Parse HTML
        info = parse(r=response)

        # Retrieve date of each event
        dates = event_dates(info[0])
        # Convert dates to datetime format
        format_dates = parse_dates(dates)
        # List of dates as string objects
        str_dates = string_dates(format_dates)
        # List of weekdays as string objects
        str_days = string_days(format_dates)

        # Band Names
        bands = band_names(info[1])

        # Event URLs
        urls = event_urls(info[1])

        # Combine info together
        event_data = combine(
            format_dates, str_dates, str_days, bands, urls, venue_name=venue
        )

        # Add gigs to big list
        res.extend(event_data)

    # Sort by datetime
    final_sort = sorted(res, key=itemgetter(0))

    # Construct table and remove first column
    df = table(gigs=final_sort)
    df2 = remove_col(df)

    # Save CSV file
    write_csv(df2)


def get_response(url):
    '''Get HTML response'''
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"} # noqa
        response = requests.get(url, headers, timeout=5)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def parse(r: requests.models.Response) -> tuple:
    """Parse HTML"""
    soup = BeautifulSoup(r.text, features="lxml")
    # Gets event date
    dates = soup.findAll("h2", class_="main-artist-event-header")
    # Gets event title & URL
    events = soup.findAll("h2", class_="main-event-header")
    return dates, events


def event_dates(dates: bs4.element.ResultSet) -> list[str]:
    # Get text from HTML
    pass_one = [date.text for date in dates]
    # Remove whitespace and line separators
    pass_two = [p.split() for p in pass_one]
    # List of cleaned dates
    pass_three = [" ".join(p[1:4]) for p in pass_two]
    return [i.replace(",", "") for i in pass_three]


def parse_dates(dates: list[str]) -> list[datetime]:
    """Convert dates into datetime format"""
    res = []
    for date in dates:
        i = datetime.strptime(date, "%d %b %Y")
        res.append(i)
    return res


def string_dates(dt_objects: list[datetime]) -> list[str]:
    """Converts datetime object into date strings"""
    res = []
    for dt in dt_objects:
        i = dt.strftime("%d-%b-%-y")
        res.append(i)
    return res


def string_days(dt_objects: list[datetime]) -> list[str]:
    """Converts datetime object into weekday"""
    res = []
    for dt in dt_objects:
        i = dt.strftime("%a")
        res.append(i)
    return res


def band_names(events: bs4.element.ResultSet) -> list[str]:
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


def combine(
    dates: list[datetime],
    string_dates: list[str],
    string_days: list[str],
    bands: list[str],
    urls: list[str],
    venue_name: str,
) -> list:
    if len(dates) == len(bands) == len(urls):
        # Create list where venue is multiplied
        venue_list = list(itertools.repeat(venue_name, len(dates)))
        return list(
            zip(dates, string_dates, string_days, bands, venue_list, urls)
        )  # noqa


def table(gigs: list) -> pd.DataFrame:
    """Table of gigs"""
    return pd.DataFrame(
        gigs, columns=["dt", "Date", "Weekday", "Event", "Venue", "Link"]
    )


def remove_col(df):
    return df.drop('dt', axis='columns')


def write_csv(df):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    filepath = f"/Users/darrenchung/Desktop/gigs_{dt_string}.csv"
    print(f"CSV file saved at {filepath}")
    return df.to_csv(filepath, index=False)


if __name__ == "__main__":
    main()
