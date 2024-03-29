from django.urls import path

from .views import AttendanceView, StudentView, TimetableView, SectionStudentView, TeacherTimetableView


app_name = "attendances"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('attendances/', AttendanceView.as_view()),
    path('student/', StudentView.as_view()),
    path('timetable/', TimetableView.as_view()),
    path('section_students/', SectionStudentView.as_view()),
    path('teacher/timetable/', TeacherTimetableView.as_view())
]