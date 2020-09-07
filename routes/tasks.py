from celery.decorators import task
import datetime
import requests
from aviatatask.celery import app
from .cache import Cache
from .data import Data
from .helpers import get_dates, get_cheapest_flight


@app.task
def update_flights():
    date_from, date_to = get_dates()
    for city_code1, city_code2 in Data.ROUTES:
        update_flight.delay(city_code1, city_code2, date_from, date_to)
        update_flight.delay(city_code2, city_code1, date_from, date_to)

@app.task
def update_flight(city_code_from, city_code_to, date_from, date_to):
    cache = Cache()

    payload = {'fly_from': city_code_from, 'fly_to': city_code_to, 'date_from': date_from, 'date_to': date_to}
    payload.update(Data.GET_FLIGHTS_DEFAULT_PARAMS)
    response = requests.get(Data.GET_FLIGHTS_URL, params=payload)

    if response.status_code != 200:
        return
    
    flights = response.json().get('data')

    if not flights:
        return

    cheapest_flight = get_cheapest_flight(flights)
    cheapest_flight_data = {}

    d_time = cheapest_flight.get('dTime')
    d_time_str = datetime.datetime.fromtimestamp(int(d_time)).strftime('%H:%M %d/%m')
    cheapest_flight_data['d_time'] = d_time_str

    a_time = cheapest_flight.get('aTime')
    a_time_str = datetime.datetime.fromtimestamp(int(a_time)).strftime('%H:%M %d/%m')
    cheapest_flight_data['a_time'] = a_time_str

    fly_duration = cheapest_flight.get('fly_duration')
    cheapest_flight_data['fly_duration'] = fly_duration

    airline = cheapest_flight.get('airlines')[0]
    cheapest_flight_data['airline'] = airline

    booking_token = cheapest_flight.get('booking_token')
    cheapest_flight_data['booking_token'] = booking_token

    flight_key = f'{city_code_from}{city_code_to}'
    cache.update_flight_info(flight_key, cheapest_flight_data)

    check_flight.delay(flight_key, booking_token)

@app.task
def check_flights():
    cache = Cache()
    tokens = cache.get_booking_tokens()
    for flight_key, token in tokens:
        check_flight.delay(flight_key, token)

@app.task
def check_flight(flight_key, token):
    cache = Cache()

    payload = {'booking_token': token}
    payload.update(Data.CHECK_FLIGHT_DEFAULT_PARAMS)
    response = requests.get(Data.CHECK_FLIGHT_URL, params=payload)

    if response.status_code != 200:
        return
    
    flight = response.json()
    
    flights_checked = flight.get('flights_checked')
    flights_invalid = flight.get('flights_invalid')
    price_change = flight.get('price_change')

    if not flights_checked:
        check_flight.delay(flight_key, token)
        return

    if price_change:
        date_from, date_to = get_dates()
        update_flight.delay(flight_key[:3], flight_key[3:], date_from, date_to)
        return

    price = flight.get('conversion').get('amount')
    check_flight_data = {'price': price, 'flights_invalid': flights_invalid}

    cache.update_flight_checked(flight_key, check_flight_data)
