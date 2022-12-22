import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup


def main():
    # Requests HTML
    request = get_html()

    # Parse HTML
    info = parse(r=request)

    # Event Dates
    dates = event_dates(info[0])

    # Band Names
    bands = band_names(info[1])

    # Event URLs
    urls = event_urls(info[1])

    # Combine info together
    event_data = combine(dates, bands, urls)

    # Show table
    df = table(event_data)


def get_html():
    # Get request from URL
    try:
        # 'https://www.moshtix.com.au/v2/venues/lazybones-lounge-restaurant-bar/7848'
        # 'https://www.moshtix.com.au/v2/venues/oxford-art-factory-sydney/867'
        url = 'https://www.moshtix.com.au/v2/venues/lazybones-lounge-restaurant-bar/7848' # noqa
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"} # noqa
        r = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.HTTPError as err:
        print(err)
    except requests.exceptions.Timeout as err:
        print(err)
    return r


def parse(r: requests.models.Response) -> tuple:
    # Parse HTML
    soup = BeautifulSoup(r.text, features='lxml')
    # Gets event date
    dates = soup.findAll('h2', class_='main-artist-event-header')
    # Gets event title & URL
    events = soup.findAll('h2', class_='main-event-header')
    return dates, events


def event_dates(dates: bs4.element.ResultSet) -> list[str]:
    # Get text from HTML
    pass_one = [date.text for date in dates]
    # Remove whitespace and line separators
    pass_two = [p.split() for p in pass_one]
    # List of cleaned dates
    return [' '.join(p[:5]) for p in pass_two]


def band_names(events: bs4.element.ResultSet) -> list[str]:
    # Get text from HTML
    pass_one = [e.text for e in events]
    # Remove whitespace and line separators
    pass_two = [p.split() for p in pass_one]
    # List of bands
    return [' '.join(p) for p in pass_two]


def event_urls(events: bs4.element.ResultSet) -> list[str]:
    urls = []
    for event in events:
        urls.extend(e['href'] for e in event.findAll('a'))
    return urls


def combine(dates: list[str], bands: list[str], urls: list[str]) -> list:
    if len(dates) == len(bands) == len(urls):
        res = list(zip(dates, bands, urls))
        print(*res, sep='\n')
        return res
    print(f"No. of Dates: {len(dates)}")
    print(f"No. of Bands: {len(bands)}")
    print(f"No. of URLs: {len(urls)}")


def table(event_data: list):
    # print('Printing table...\n')
    return pd.DataFrame(data=event_data, columns=['Date', 'Event', 'Link'])


if __name__ == '__main__':
    main()
