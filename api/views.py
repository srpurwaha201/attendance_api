from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_firebase_auth.authentication import FirebaseAuthentication

from .models import Attendance, Timetable, Student, Teacher, Section
from .serializers import AttendanceSerializer, SectionSerializer, StudentSerializer, TimetableSerializer, TeacherSerializer

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
    authentication_classes = [FirebaseAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        # print("roll no is -------------> ",request.data.get('rollno'))
        # rollno = request.data.get('rollno')
        email = request.GET["email"]
        student = Student.objects.get(email = email)
        # print("studet is ------------------------>",student.name)
        sections = student.section_set.all()
        studentserializer = StudentSerializer(student)
        sectionserializer = SectionSerializer(sections, many=True)
        for i in sectionserializer.data:
            total = len(Attendance.objects.filter(timetable__section__slot = i['slot']))
            present = len(student.attendance_set.all().filter(timetable__section__slot = i['slot']))
            i['total'] = total
            i['present'] = present

        return Response({"Student":studentserializer.data, "Sections":sectionserializer.data})

class TimetableView(APIView):
    def get(self, request):
        email = request.GET['email']
        student = Student.objects.get(email=email)
        sections = student.section_set.all()
        # studentserializer = StudentSerializer(student)
        # sectionserializer = SectionSerializer(sections, many=True)
        response = {"Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[]}
        for i in sections:
            # print(i)
            timetables = i.timetable_set.all()
            timetableserializer = TimetableSerializer(timetables, many=True)
            for j in timetableserializer.data:
                # print(j)
                response[j['day']].append(j)

        for _, value in response.items():
            value.sort(key=lambda item:item['startTime'])
        return Response(response)

class SectionStudentView(APIView):
    def get(self, request):
        email = request.GET['email']
        teacher = Teacher.objects.get(email=email)
        teacherserializer = TeacherSerializer(teacher)
        section = teacher.section_set.all().filter(slot = request.GET['slot'])[0]
        sectionserializer = SectionSerializer(section)
        students = section.students.all()
        studentsserializer = StudentSerializer(students, many=True)
        return Response({"Teacher": teacherserializer.data, "Section": sectionserializer.data, "Students":studentsserializer.data})


class TeacherTimetableView(APIView):
    # authentication_classes = [FirebaseAuthentication]
    def get(self, request):
        email = request.GET['email']
        teacher = Teacher.objects.get(email=email)
        sections = teacher.section_set.all()
        # studentserializer = StudentSerializer(student)
        # sectionserializer = SectionSerializer(sections, many=True)
        response = {"Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[]}
        for i in sections:
            # print(i)
            timetables = i.timetable_set.all()
            timetableserializer = TimetableSerializer(timetables, many=True)
            for j in timetableserializer.data:
                del j['section']['teacher']
                response[j['day']].append(j)

        for _, value in response.items():
            value.sort(key=lambda item:item['startTime'])
        return Response(response)