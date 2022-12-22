import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup


def main():
    # Requests HTML
    request = get_html()

    # Parse HTML
    ids = parse(r=request)

    # Get Dates and Event Names
    info = event_info(ids)
    print(*info, sep='\n')


def get_html():
    # Get request from URL
    try:
        url = 'https://www.factorytheatre.com.au/?s&key=upcoming'  # noqa
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}  # noqa
        r = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.HTTPError as err:
        print(err)
    except requests.exceptions.Timeout as err:
        print(err)
    return r


def parse(r: requests.models.Response) -> list[str]:
    # Parse HTML
    soup = BeautifulSoup(r.text, features='lxml')
    # Get unique IDs
    return [tag['id'] for tag in soup.select('a[id]')]


def event_info(ids: list[str]) -> tuple:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}  # noqa

    urls = []
    dates = []
    events = []
    for i in ids:
        url = f"https://www.factorytheatre.com.au/event/{i}/"
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, features='lxml')

        # Get URLs
        urls.append(url)

        # Get event's date
        date = soup.find('li', class_='session-date').text
        dates.append(date)

        # Get event name
        event = soup.find('h1', class_='title').text
        events.append(event)

    return list(zip(dates, events, urls))


if __name__ == '__main__':
    main()
