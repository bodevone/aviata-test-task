from django.core.cache import cache

class Data:
    NAMES = {
        'ALA': ['Almaty', 'Алматы'],
        'TSE': ['Astana', 'Астана', 'Nur-Sultan', 'Нур-Султан'],
        'MOW': ['Moscow', 'Москва'],
        'CIT': ['Shymkent', 'Шымкент'],
        'LED': ['Saint Petersburg', 'Санкт-Петербург']
    }

    ROUTES = (
        ('ALA', 'TSE'),
        ('TSE', 'ALA'),
        ('ALA', 'MOW'),
        ('MOW', 'ALA'),
        ('ALA', 'CIT'),
        ('CIT', 'ALA'),
        ('TSE', 'MOW'),
        ('MOW', 'TSE'),
        ('TSE', 'LED'),
        ('LED', 'TSE'),
    )

    GET_FLIGHTS_URL = 'https://api.skypicker.com/flights'
    GET_FLIGHTS_DEFAULT_PARAMS = {
        'partner': 'picky',
        'curr': 'KZT'
    }

    CHECK_FLIGHT_URL = 'https://booking-api.skypicker.com/api/v0.1/check_flights'
    CHECK_FLIGHT_DEFAULT_PARAMS = {
        'bnum': 1,
        'pnum': 1,
        'currency': 'KZT'
    }

    GET_FLIGHTS_TIMEOUT = 24 * 60 * 60
