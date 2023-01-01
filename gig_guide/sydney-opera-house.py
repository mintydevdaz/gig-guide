import requests
from datetime import date


def main():
    # Construct URL with unique date range
    url = get_url()

    # Request HTML
    r = get_html(url)

    # Get JSON
    json = get_json(response=r)

    # Cycle through each event
    res = []
    for j in json['data']['tiles']:
        date = event_date(j)
        event = event_name(j)
        url = event_url(j)
        res.append((date, event, url))

    # Show event info
    print(*res[1:], sep='\n')


def get_url() -> str:
    '''Constructs URL from today's date. Date range is 1+ year'''
    d = date.today()
    next_year = f'{str(d.year + 1)}-{str(d.month)}-{str(d.day)}'
    return f"https://www.sydneyoperahouse.com/bin/soh/whatsOnFilter?filterPaths=%2Fcontent%2Fsoh%2Fevents%2C%2Fcontent%2Fsoh%2Fevents%2Fwhats-on%2C%2Fcontent%2Fsoh%2Fevents%2Fwhats-on%2Fopera-australia%2F2022%2C%2Fcontent%2Fsoh%2Fevents%2Fwhats-on%2FAntidote%2F2022%2C%2Fcontent%2Fsoh%2Fevents%2Fwhats-on%2Faustralian-chamber-orchestra%2F2022-season&loadMoreNext=14&duration=14&filterType=1&limit=6&offset=0&fromDate={str(d)}&toDate={next_year}&genres=event-type%3Acontemporary-music" # noqa


def get_html(url: str) -> requests.models.Response:
    '''Request HTML'''
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}  # noqa
        r = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.HTTPError as e:
        print(e)
    except requests.exceptions.Timeout as e:
        print(e)
    return r


def get_json(response: requests.models.Response) -> dict:
    '''Gets JSON file'''
    return response.json()


def event_date(json: dict) -> str:
    '''Extracts date and time of event'''
    j = json['schedules'][0].get('performanceDate')
    date, time = j.split('T')
    return f'{date}, {time}'


def event_name(json: dict) -> str:
    '''Extracts name of event'''
    return json.get('title')


def event_url(json: dict) -> str:
    '''Extracts & builds the event's url'''
    link = json['description'].get('ctaURL')
    return f"https://www.sydneyoperahouse.com{link}"


if __name__ == '__main__':
    main()
