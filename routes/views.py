from django.shortcuts import render
from django.http import Http404
from .cache import Cache
from .helpers import get_key_from_cities


def indexPage(request):
    cache = Cache()
    if 'fly_from' in request.GET and 'fly_to' in request.GET and 'date' in request.GET:
        from_city = request.GET['fly_from']
        to_city = request.GET['fly_to']
        date = request.GET['date']
        search = get_key_from_cities(from_city, to_city, date)
        if not search:
            raise Http404

        flight = cache.get_flight_from_key(search)
        if not flight:
            raise Http404
        context = {'flights': [flight]}
    elif 'fly_from' in request.GET or 'fly_to' in request.GET or 'date' in request.GET:
        raise Http404
    else:
        flights = cache.get_all_flights()
        context = {'flights': flights}

    return render(request, 'index.html', context)