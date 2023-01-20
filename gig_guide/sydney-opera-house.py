import requests
import itertools
from datetime import date, datetime


def main():
    # Constructs unique URL
    url = create_url()

    # Request HTML
    r = get_response(url)

    # Get JSON
    json = get_json(response=r)

    # Cycle through each event
    dates = []
    events = []
    urls = []
    for j in json["data"]["tiles"]:
        d = event_date(j)
        e = event_name(j)
        u = event_url(j)
        dates.append(d)
        events.append(e)
        urls.append(u)

    # Convert dates to datetime objects
    dt = convert_dt(dates)
    # Format dates (dd-mmm-yyyy) and weekday
    str_dates = string_dates(dt)
    str_days = string_weekdays(dt)

    # Generate list with venue name
    venue_list = list(itertools.repeat("Sydney Opera House", len(dates)))

    # Create table
    table = prepare_table(
        datetime_objects=dt,
        str_dates=str_dates,
        weekday=str_days,
        events=events,
        venue=venue_list,
        urls=urls,
    )

    print(*table[1:], sep="\n")


def create_url() -> str:
    """
    Constructs URL from today's date where the date range spans from today
    +1 year.
    """
    d = date.today()
    next_year = f"{str(d.year + 1)}-{str(d.month)}-{str(d.day)}"
    return f"https://www.sydneyoperahouse.com/bin/soh/whatsOnFilter?filterPaths=%2Fcontent%2Fsoh%2Fevents%2C%2Fcontent%2Fsoh%2Fevents%2Fwhats-on%2C%2Fcontent%2Fsoh%2Fevents%2Fwhats-on%2Fopera-australia%2F2022%2C%2Fcontent%2Fsoh%2Fevents%2Fwhats-on%2FAntidote%2F2022%2C%2Fcontent%2Fsoh%2Fevents%2Fwhats-on%2Faustralian-chamber-orchestra%2F2022-season&loadMoreNext=14&duration=14&filterType=1&limit=6&offset=0&fromDate={str(d)}&toDate={next_year}&genres=event-type%3Acontemporary-music"  # noqa


def get_response(url: str) -> requests.models.Response:
    """Get HTML response"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }  # noqa
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        return r
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def get_json(response: requests.models.Response) -> dict:
    """Get JSON file"""
    return response.json()


def event_date(json: dict) -> str:
    """Extracts date of event"""
    j = json["schedules"][0].get("performanceDate")
    date, time = j.split("T")
    return date


def event_name(json: dict) -> str:
    """Extracts name of event"""
    return json.get("title")


def event_url(json: dict) -> str:
    """Extracts & builds the event's url"""
    link = json["description"].get("ctaURL")
    return f"https://www.sydneyoperahouse.com{link}"


def convert_dt(dates: list[str]) -> list[datetime]:
    """Parse dates into datetime objects"""
    dt_objects = []
    for d in dates:
        i = datetime.strptime(d, "%Y-%m-%d")
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
