from django.db import models

class Student(models.Model):
    rollno = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField()


class Teacher(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField()

class Subject(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, null=False)


class Section(models.Model):
    #will include slot like CO402-P
    slot = models.CharField(primary_key=True, max_length=10)
    subject = models.ForeignKey(Subject, null=False,on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,blank=False)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)


class Timetable(models.Model):
    section = models.ForeignKey(Section, null=False,on_delete=models.CASCADE)
    day = models.CharField(max_length=10, null=False)
    startTime = models.TimeField()
    endTime = models.TimeField()
    location = models.CharField(max_length = 50)

class Attendance(models.Model):
    timetable = models.ForeignKey(Timetable,on_delete=models.CASCADE)
    date = models.DateField()
    #students contain only present students. Total no. of class will be calculated using current date and timetable.
    #total % will be calculated accordingly
    students = models.ManyToManyField(Student)
