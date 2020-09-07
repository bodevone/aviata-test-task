from django.core.cache import cache
from .data import Data
from .helpers import get_flight_key

class Cache:
    """
    Model with methods for interaction with cache
    name_ : city name -> city code
    flight_ : from city + to city -> info about flight
    token_ : booking_token -> available, price change
    """
    def get_key_from_places(self, from_city, to_city):
        "Get key from pair of cities"
        if from_city in Data.NAMES and to_city in Data.NAMES:
            from_city_code = from_city
            to_city_code = to_city
        elif from_city in Data.NAMES:
            from_city_code = from_city
            to_city_code = cache.get(f'name_{to_city}')
        elif to_city in Data.NAMES:
            to_city_code = to_city
            from_city_code = cache.get(f'name_{from_city}')

        if not from_city_code or not to_city_code:
            return
        key = get_flight_key(from_city_code, to_city_code)
        return key

    def get_flight_from_key(self, key):
        flight = self.get_flight(f'flight_{key}')
        if not flight:
            return
        return flight
    
    def get_all_flights(self):
        flights = []
        flights_keys = cache.keys('flight_*')
        for key in flights_keys:
            flight = self.get_flight(key)
            flights.append(flight)
        return flights

    def get_flight(self, flight_key):
        key = flight_key[7:]
        flight_data = cache.get(flight_key)
        if not flight_data:
            return
        check_flight_data = cache.get(f'checked_{key}')
        if check_flight_data:
            flight_data.update(check_flight_data)
        flight_data.update({'fly_from': key[:3], 'fly_to': key[3:]})
        return flight_data
    
    def get_booking_tokens(self):
        tokens = []
        tokens_keys = cache.keys('token_*')
        for key in tokens_keys:
            token = cache.get(key)
            tokens.append((key[6:], token))
        return tokens
    
    def flight_checked(self, flight_key, check_flight_data):
        cache.set(f'checked_{flight_key}', check_flight_data, timeout=Data.GET_FLIGHTS_TIMEOUT)
        
    def update_flight_info(self, flight_key, flight_data):
        cache.set(f'flight_{flight_key}', flight_data, timeout=Data.GET_FLIGHTS_TIMEOUT)

    def populate_names(self):
        '''Store name to code'''
        for code, names in Data.NAMES:
            for name in names:
                cache.set(f'name_{name}', code, timeout=None)