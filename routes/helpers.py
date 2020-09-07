import requests
import datetime
import calendar
from .data import Data


def get_cheapest_flight(flights):
    cheapest_flight = {}
    for flight in flights:
        if not cheapest_flight or cheapest_flight.get('price') > flight.get('price'):
            cheapest_flight = flight
    return cheapest_flight

def get_flight_key(city_code_from, city_code_to):
    return f'{city_code_from}{city_code_to}'

def get_dates():
    this_date = datetime.datetime.today()
    next_date = get_next_month(this_date)
    date_from = this_date.strftime('%d/%m/%Y')
    date_to = next_date.strftime('%d/%m/%Y')
    return date_from, date_to

def get_next_month(this_date):
    next_year = this_date.year
    next_month = this_date.month + 1
    if next_month > 12:
        next_year += 1
        next_month = 1
    last_day_of_next_month = calendar.monthrange(next_year, next_month)[1]
    next_day = min(this_date.day, last_day_of_next_month)
    next_date = this_date.replace(year=next_year, month=next_month, day=next_day)
    return next_date
