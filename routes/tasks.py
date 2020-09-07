import requests
from aviatatask.celery import app
from .cache import Cache
from .data import Data
from .helpers import get_dates, get_cheapest_flight, format_from_timestamp


@app.task
def update_flights():
    dates = get_dates()
    for date in dates:
        for city_code1, city_code2 in Data.ROUTES:
            update_flight.delay(city_code1, city_code2, date)
            update_flight.delay(city_code2, city_code1, date)

@app.task
def update_flight(city_code_from, city_code_to, date):
    cache = Cache()

    payload = {'fly_from': city_code_from, 'fly_to': city_code_to, 'date_from': date, 'date_to': date}
    payload.update(Data.GET_FLIGHTS_DEFAULT_PARAMS)
    response = requests.get(Data.GET_FLIGHTS_URL, params=payload)

    if response.status_code != 200:
        return
    
    flights = response.json().get('data')
    if not flights:
        return

    cheapest_flight = flights[0]
    cheapest_flight_data = {}

    d_time = cheapest_flight.get('dTime')
    cheapest_flight_data['d_time'] = format_from_timestamp(d_time)

    a_time = cheapest_flight.get('aTime')
    cheapest_flight_data['a_time'] = format_from_timestamp(a_time)

    fly_duration = cheapest_flight.get('fly_duration')
    cheapest_flight_data['fly_duration'] = fly_duration

    airlines = ''
    for airline in cheapest_flight.get('airlines'):
        if airlines:
            airlines += ' '
        airlines += airline
    cheapest_flight_data['airlines'] = airlines

    booking_token = cheapest_flight.get('booking_token')
    cheapest_flight_data['booking_token'] = booking_token

    flight_key = f'{city_code_from}{city_code_to}{date}'
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
        update_flight.delay(flight_key[:3], flight_key[3:6], flight_key[6:])
        return

    price = flight.get('conversion').get('amount')
    check_flight_data = {'price': price, 'flights_invalid': flights_invalid}

    cache.update_flight_checked(flight_key, check_flight_data)
