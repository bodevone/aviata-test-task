from django.core.cache import cache
from .data import Data

class Cache:
    """
    Model with methods for interaction with cache
    flight_ : from city + to city -> data about flight
    checked_ : from city + to city -> data about price and availability of flight
    """
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
        flight_data.update({'fly_from': key[:3], 'fly_to': key[3:6]})
        return flight_data
    
    def get_booking_tokens(self):
        tokens = []
        flight_keys = cache.keys('flight_*')
        for key in flight_keys:
            token = cache.get(key).get('booking_token')
            tokens.append((key[7:], token))
        return tokens
    
    def update_flight_checked(self, flight_key, check_flight_data):
        cache.set(f'checked_{flight_key}', check_flight_data, timeout=Data.CACHE_TIMEOUT)
        
    def update_flight_info(self, flight_key, flight_data):
        cache.set(f'flight_{flight_key}', flight_data, timeout=Data.CACHE_TIMEOUT)