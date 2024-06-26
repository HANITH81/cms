from django.contrib import admin
from .models import Course,Faculty,FacultyCourseClass,Student,CollegeClass,Attendance

admin.site.register(Course)
admin.site.register(Faculty)
admin.site.register(FacultyCourseClass)
admin.site.register(CollegeClass)
admin.site.register(Attendance)
admin.site.register(Student)
