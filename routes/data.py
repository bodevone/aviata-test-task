from django.core.cache import cache

class Data:
    """Class to store global data about cities, routes and requests"""
    
    "To check for city code in search query"
    CITY_CODES = {'ALA', 'TSE', 'MOW', 'CIT', 'LED'}

    "To match from search query to city code"
    CITY_NAMES_TO_CODES = {
        'Almaty': 'ALA',
        'Astana': 'TSE',
        'Moscow': 'MOW',
        'Shymkent': 'CIT',
        'Saint Petersburg': 'LED'
    }

    ROUTES = (
        ('ALA', 'TSE'),
        ('TSE', 'ALA'),
        # ('ALA', 'MOW'),
        # ('MOW', 'ALA'),
        # ('ALA', 'CIT'),
        # ('CIT', 'ALA'),
        # ('TSE', 'MOW'),
        # ('MOW', 'TSE'),
        # ('TSE', 'LED'),
        # ('LED', 'TSE'),
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

    "To store flight data in cache for 24 hours"
    CACHE_TIMEOUT = 24 * 60 * 60
