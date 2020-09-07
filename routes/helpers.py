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

def get_key_from_cities(from_city, to_city):
    """Return key from cities codes or names"""
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

    key = f'{from_city_code}{to_city_code}'
    return key
    
def get_dates():
    """Return pair of dates of current and next months"""
    this_date = datetime.datetime.today()
    next_date = get_next_month(this_date)
    date_from = this_date.strftime('%d/%m/%Y')
    date_to = next_date.strftime('%d/%m/%Y')
    return date_from, date_to

def get_next_month(this_date):
    """Return date of the same day of the next month"""
    next_year = this_date.year
    next_month = this_date.month + 1
    if next_month > 12:
        next_year += 1
        next_month = 1
    last_day_of_next_month = calendar.monthrange(next_year, next_month)[1]
    next_day = min(this_date.day, last_day_of_next_month)
    next_date = this_date.replace(year=next_year, month=next_month, day=next_day)
    return next_date
