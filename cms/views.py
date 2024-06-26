from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import AttendanceSerializer,StudentSerializer,FacultySerializer,ClassSerializer

from .models import Course, Faculty, FacultyCourseClass, CollegeClass, Attendance, Student

@api_view(['GET'])
def home(request):
    routes = [
        {
            'Name': 'Hanith'
        },
        {
            'Name': 'Rajesh'
        }
    ]
    return Response(routes)


@api_view(['GET'])
def faculty_s(request):
    f = Faculty.objects.all()
    fs = FacultySerializer(f,many=True)
    return Response(fs.data,status = status.HTTP_200_OK)


class FacultyAttendanceAPIView(APIView):
    def get(self,request,rollno, *args,**kwargs):
        faculty = Faculty.objects.get(rollno=rollno)

        classes = CollegeClass.objects.filter(facultycourseclass__faculty = faculty)

        class_serializer = ClassSerializer(classes,many=True)

        return Response(class_serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, rollno, class_code, *args, **kwargs):
        try:

            faculty = Faculty.objects.get(rollno=rollno)
            college_class = CollegeClass.objects.get(code=class_code)
            faculty_course_class = FacultyCourseClass.objects.get(faculty=faculty, class_name=college_class)
            course = faculty_course_class.course

            st = Student.objects.get(roll_no = request.data.get('rollno'))

            attendance_data = {
                'faculty': faculty.id,
                'course': course.id,
                'class_name': college_class.id,
                'student':st.id,
                'date': request.data.get('date'),  
                'is_present': request.data.get('is_present'),
            }

            attendance_serializer = AttendanceSerializer(data=attendance_data)
            if attendance_serializer.is_valid():
                attendance_serializer.save()
                return Response({'detail': 'Attendance posted successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)

        except Faculty.DoesNotExist:
            return Response({'error': 'Faculty not found.'}, status=status.HTTP_404_NOT_FOUND)
        except CollegeClass.DoesNotExist:
            return Response({'error': 'CollegeClass not found.'}, status=status.HTTP_404_NOT_FOUND)
        except FacultyCourseClass.DoesNotExist:
            return Response({'error': 'FacultyCourseClass not found for the given faculty and class.'}, status=status.HTTP_404_NOT_FOUND)
        
        
class StudentAttendanceAPIView(APIView):
    def get(self, request, rollno, *args, **kwargs):
        try:
            student = Student.objects.get(roll_no=rollno)

            enrolled_class = student.enrolled_class

            enrolled_courses_dict = {}
            faculty_course_classes = FacultyCourseClass.objects.filter(class_name_id=enrolled_class.id)
            for faculty_course_class in faculty_course_classes:
                enrolled_courses_dict[faculty_course_class.course.name] = faculty_course_class

            course_attendance_info = {}
            absent_classes_list = []


            for course_name, enrolled_course_class in enrolled_courses_dict.items():
      
                course_attendance = Attendance.objects.filter(student=student, course=enrolled_course_class.course)

                total_classes_held = course_attendance.count()

                classes_attended = course_attendance.filter(is_present=True).count()
           
                attendance_percentage = 0 if total_classes_held == 0 else (classes_attended / total_classes_held) * 100

                course_attendance_info[course_name] = {
                    'total_classes_held': total_classes_held,
                    'classes_attended': classes_attended,
                    'attendance_percentage': attendance_percentage,
                }

                absent_classes = course_attendance.filter(is_present=False)
                for absent_class in absent_classes:
                    absent_classes_list.append({
                        'course': course_name,
                        'class_date': absent_class.date,
                    })

            overall_attendance_percentage = sum(
                info['attendance_percentage'] for info in course_attendance_info.values()
            ) / len(course_attendance_info) if course_attendance_info else 0

            return Response({
                'student_name': student.name,
                'overall_attendance_percentage': overall_attendance_percentage,
                'absent_classes_list': absent_classes_list,
                'course_attendance_info': course_attendance_info,
            }, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
