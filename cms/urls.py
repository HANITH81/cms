from django.urls import path
from . import views
from .views import FacultyAttendanceAPIView,StudentAttendanceAPIView

urlpatterns = [
    path('',views.home),
    path('faculty/',views.faculty_s,name='facultys'),
    path('faculty/<str:rollno>/',FacultyAttendanceAPIView.as_view(), name='faculty_classes'),
    path('faculty/<str:rollno>/<str:class_code>/',FacultyAttendanceAPIView.as_view(), name='attendance_posting'),
    path('student/<str:rollno>/',StudentAttendanceAPIView.as_view(),name='attendance_view'),
]