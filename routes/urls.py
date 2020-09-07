from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexPage, name='index'),
]