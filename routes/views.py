from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views import View
from .cache import Cache


def indexPage(request):
    cache = Cache()
    if 'fly_from' in request.GET and 'fly_to' in request.GET:
        from_place = request.GET['fly_from']
        to_place = request.GET['fly_to']
        search = cache.get_key_from_places(from_place, to_place)
        if not search:
            raise Http404

        flight = cache.get_flight_from_key(search)
        if not flight:
            raise Http404
        context = {'flights': [flight]}

    elif 'fly_from' in request.GET or 'fly_to' in request.GET:
        raise Http404
    else:
        flights = cache.get_all_flights()
        context = {'flights': flights}

    return render(request, 'index.html', context)