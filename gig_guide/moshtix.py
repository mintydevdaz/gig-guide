import itertools
from datetime import datetime
from operator import itemgetter

import bs4
import requests
from bs4 import BeautifulSoup
from moshtix_urls import urls


def main():
    global urls
    res = []
    for venue, url in urls.items():

        # Requests HTML
        request = get_html(url)

        # Parse HTML
        info = parse(r=request)

        # Retrieve date of each event
        dates = event_dates(info[0])

        # Convert dates to datetime format
        format_dates = parse_dates(dates)

        # Band Names
        bands = band_names(info[1])

        # Event URLs
        urls = event_urls(info[1])

        # Combine info together
        event_data = combine(format_dates, bands, urls, venue_name=venue)

        # Add gigs to big list
        res.extend(event_data)

    # Sort by datetime
    final_sort = sorted(res, key=itemgetter(0))
    print(final_sort, sep='\n')


def get_html(url):
    """Request HTML"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.HTTPError as err:
        print(err)
    except requests.exceptions.Timeout as err:
        print(err)
    return r


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
    dates: list[str], bands: list[str], urls: list[str], venue_name: str
) -> list:
    if len(dates) == len(bands) == len(urls):
        # Create list where venue is multiplied
        venue_list = list(itertools.repeat(venue_name, len(dates)))
        return list(zip(dates, bands, venue_list, urls))


if __name__ == "__main__":
    main()
