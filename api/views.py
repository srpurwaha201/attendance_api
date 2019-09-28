from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Attendance, Timetable, Student
from .serializers import AttendanceSerializer, SectionSerializer, StudentSerializer

class AttendanceView(APIView):
    def get(self, request):
        attendances = Attendance.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = AttendanceSerializer(attendances, many=True)
        # return Response({"articles": serializer.data})
        return Response({"attendances": serializer.data})

        # students = Student.objects.all()
        # serializer = StudentSerializer(students, many=True)
        # return Response({"students":serializer.data})

    def post(self, request):
        #pass timetable id, date, and list of roll nos present in the class
        timetableid = request.data.get('timetableid')[0]
        timetable = Timetable.objects.get(id=timetableid)
        date = request.data.get('date')
        rollnos = request.data.get('rollnos')

        print(rollnos)
        attendance = Attendance.objects.create(timetable = timetable, date = date)
        for r in rollnos:
            attendance.students.add(Student.objects.get(rollno = r))
        
        attendance.save()
        # attendance = request.data.get('attendance')

        # Create an article from the above data
        # serializer = AttendanceSerializer(data=attendance)
        # if serializer.is_valid(raise_exception=True):
        #     attendance_saved = serializer.save()
        # return Response({"success": "Attendance for '{}' created successfully".format(attendance_saved.date)})

        return Response({"success":""})

class StudentView(APIView):
    def get(self, request):
        print("roll no is -------------> ",request.data.get('rollno'))
        rollno = request.data.get('rollno')
        student = Student.objects.get(rollno = rollno)
        # print("studet is ------------------------>",student.name)
        sections = student.section_set.all()
        studentserializer = StudentSerializer(student)
        sectionserializer = SectionSerializer(sections, many=True)
        return Response({"Student":studentserializer.data, "Sections":sectionserializer.data})