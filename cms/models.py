from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser



# Course model
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

# Faculty model
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rollno = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.user.username

# Class model
class CollegeClass(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class FacultyCourseClass(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_name = models.ForeignKey(CollegeClass, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('faculty', 'course')
        constraints = [
            models.UniqueConstraint(fields=['faculty', 'class_name'], name='unique_faculty_class')
        ]


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    roll_no = models.CharField(max_length = 10, unique= True)
    enrolled_class = models.ForeignKey(CollegeClass, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

# Attendance model
class Attendance(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_name = models.ForeignKey(CollegeClass, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student} - {self.date} - {'Present' if self.is_present else 'Absent'}"



