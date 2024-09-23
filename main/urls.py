from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("appointment/", views.make_appointment, name="appointment"),
    path("report_errors", views.report_errors, name="report_errors"),
    path(
        "get-available-slots/",
        views.get_available_slots_view,
        name="get_available_slots",
    ),  # API endpoint for getting available slots for a given date.
]
