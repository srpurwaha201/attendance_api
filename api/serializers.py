from rest_framework import serializers
from .models import Student, Subject, Teacher, Section, Attendance, Timetable

# class TrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Track
#         fields = ['order', 'title', 'duration']

class StudentSerializer(serializers.Serializer):
    rollno = serializers.CharField()
    name = serializers.CharField()
    
    class Meta:
        model = Student
        fields = ['rollno','name']

class SubejctSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    class Meta:
        model = Subject
        fields = ['code', 'name']

class TeacherSerializer(serializers.Serializer):
    name = serializers.CharField()
    class Meta:
        model = Teacher
        fields = ['name']

class SectionSerializer(serializers.Serializer):
    subject = SubejctSerializer( read_only=True)
    teacher = TeacherSerializer(read_only=True)
    slot = serializers.CharField()
    class Meta:
        model = Section
        fields = ['slot','subject','teacher']

class TimetableSerializer(serializers.Serializer):
    section = SectionSerializer(read_only=True)
    day = serializers.CharField()
    startTime = serializers.TimeField()
    endTime = serializers.TimeField()
    class Meta:
        model = Timetable
        fields = ['section', 'day','startTime','endTime']

    
class AttendanceSerializer(serializers.Serializer):
    # title = serializers.CharField(max_length=120)
    # description = serializers.CharField()
    # body = serializers.CharField()

    timetable = TimetableSerializer(read_only=True)
    date = serializers.DateField()
    students = StudentSerializer(many = True, read_only=True)

    
    def create(self, validated_data):
        print("here")
        print()
        return Attendance.objects.create(**validated_data)
    
    #students contain only present students. Total no. of class will be calculated using current date and timetable.
    #total % will be calculated accordingly
    class Meta:
        model = Attendance
        fields = ['timetable', 'date', 'students']