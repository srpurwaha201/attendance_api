from django.urls import path

from .views import AttendanceView, StudentView, TimetableView


app_name = "attendances"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('attendances/', AttendanceView.as_view()),
    path('student/', StudentView.as_view()),
    path('timetable/', TimetableView.as_view())
]