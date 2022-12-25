import bs4
import requests
from bs4 import BeautifulSoup


def main():
    urls = ['https://www.enmoretheatre.com.au/?s&key=upcoming',
            'https://www.metrotheatre.com.au/?s&key=upcoming',
            'https://www.factorytheatre.com.au/?s&key=upcoming',
            'https://www.theconcourse.com.au/?s&key=upcoming',
            'https://www.manningbar.com/?s&key=upcoming'
            ]

    dates = []
    events = []
    links = []
    for idx, url in enumerate(urls, start=1):

        # !! DELETE
        print(f'Getting data:\n{idx}. {url}')

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

    # Combine event info together
    info = combine_data(dates, events, links)
    print(*info, sep='\n')


def get_html(url: str) -> requests.models.Response:
    # Get request from URL
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}  # noqa
        r = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.HTTPError as err:
        print(err)
    except requests.exceptions.Timeout as err:
        print(err)
    return r


def parse(r: requests.models.Response) -> bs4.element.ResultSet:
    '''Parse HTML'''
    return BeautifulSoup(r.text, features='lxml')


def get_html_ids(soup: bs4.element.ResultSet) -> list[str]:
    '''Get unique HTML ids'''
    return [tag['id'] for tag in soup.select('a[id]')]


def get_new_url(url: str, html_id: str) -> str:
    link = url.removesuffix('?s&key=upcoming')
    return f'{link}event/{html_id}/'


def event_date(soup: bs4.element.ResultSet) -> str:
    return soup.find('li', class_='session-date').text


def event_name(soup: bs4.element.ResultSet) -> str:
    return soup.find('h1', class_='title').text


def combine_data(dates: list[str], events: list[str], links: list[str]) -> list:
    return list(zip(dates, events, links))


if __name__ == '__main__':
    main()
