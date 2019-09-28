from django.urls import path

from .views import AttendanceView


app_name = "attendance"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('attendances/', AttendanceView.as_view()),
]