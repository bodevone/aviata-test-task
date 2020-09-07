import datetime
import calendar
from .data import Data


def get_cheapest_flight(flights):
    """Return cheapest flight from response of request"""
    cheapest_flight = {}
    for flight in flights:
        if not cheapest_flight or cheapest_flight.get('price') > flight.get('price'):
            cheapest_flight = flight
    return cheapest_flight

def get_key_from_cities(from_city, to_city, date):
    """Return key from cities codes or names and date"""
    if from_city in Data.CITY_CODES:
        from_city_code = from_city
    else:
        from_city_code = Data.CITY_NAMES_TO_CODES.get(from_city)

    if to_city in Data.CITY_CODES:
        to_city_code = to_city
    else:
        to_city_code = Data.CITY_NAMES_TO_CODES.get(to_city)

    if not from_city_code or not to_city_code:
        return

    key = f'{from_city_code}{to_city_code}{date}'
    return key
    
def get_dates():
    """Return dates from current date up to next month"""
    curr_date = datetime.datetime.today()
    curr_day = curr_date.day
    dates = []
    while not dates or curr_date.day != curr_day:
        dates.append(format_from_datetime(curr_date))
        curr_date += datetime.timedelta(days=1)
    dates.append(format_from_datetime(curr_date))
    return dates

def format_from_datetime(date):
    """Return formatted date string from datetime object"""
    return date.strftime('%d/%m/%Y')

def format_from_timestamp(date_str):
    """Return formatted date string from UTC timestamp string"""
    formatted_date_str = datetime.datetime.fromtimestamp(int(date_str)).strftime('%H:%M %d/%m')
    return formatted_date_str
