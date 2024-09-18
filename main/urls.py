from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('appointment/', views.make_appointment, name='appointment'),
    path('success/', views.make_success, name='success'),
    path('get_available_slots/', views.get_available_slots, name='get_available_slots'),  # API endpoint for getting available slots for a given date.
]