from rest_framework.serializers import ModelSerializer

from .models import Attendance,Student,FacultyCourseClass,CollegeClass,Faculty


class ClassSerializer(ModelSerializer):
    class Meta:
        model = CollegeClass
        fields = '__all__'

class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class FacultySerializer(ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['rollno']