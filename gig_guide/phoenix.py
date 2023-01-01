import re
import requests
import bs4
from bs4 import BeautifulSoup


def main():
    # Request HTML
    main_page = 'https://phoenixcentralpark.com.au/season-vii'
    request = get_html(url=main_page)

    # Parse HTML
    soup = parse(r=request)

    # Extract individual event URLs
    urls = get_urls(soup)

    # Extract event details
    event = []
    for url in urls:
        # Get HTML & parse
        request = get_html(url)
        soup = parse(request)
        # Get headline act & date
        date = event_date(soup)
        name = event_act(soup)
        # Add event details to list
        event.append((date, name, url))

    print(*event, sep='\n')


def get_html(url):
    '''Request HTML'''
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}  # noqa
        r = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.HTTPError as err:
        print(err)
    except requests.exceptions.Timeout as err:
        print(err)
    return r


def parse(r: requests.models.Response) -> bs4.BeautifulSoup:
    '''Parse HTML'''
    return BeautifulSoup(r.text, features='lxml')


def get_urls(soup: bs4.BeautifulSoup) -> list[str]:
    '''Obtain event URLs from webpage'''
    links = [link['href'] for link in soup.findAll('a', href=True)]
    return list({url for url in links if 'https://phoenixcentralpark.com.au' in url})


def event_date(soup: bs4.BeautifulSoup) -> str:
    '''Obtain date and time of event'''
    extract = soup.findAll('p', class_='sqsrte-large')
    date = extract[-1].text if len(extract) != 1 else extract[0].text
    d = re.split('(2023)', date)
    return f'{d[0]}{d[1]}, {d[-1]}'


def event_act(soup: bs4.BeautifulSoup) -> str:
    ''''''
    return soup.find('h1').text


if __name__ == "__main__":
    main()
