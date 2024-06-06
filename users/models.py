from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stu_no = models.CharField(verbose_name="Student Number", max_length=10, blank=False, null=False)
    is_ta = models.BooleanField(default=False)
    phone_no = models.CharField(verbose_name="Phone Number", blank=False, null=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', verbose_name="Profile Picture", blank=True, null=True)
    rate_sum = models.IntegerField(verbose_name="Rating Sum",default=0)
    rate_count = models.IntegerField(verbose_name="Rating Count",default=0)
    average = models.IntegerField(verbose_name="Rating Count",default=0)
    university = models.CharField(verbose_name='University', max_length=20, default='')
    college = models.CharField(verbose_name='College', max_length=20, default='')
    about_me = models.TextField(verbose_name='About Me', default='')
    gpa = models.FloatField(verbose_name='GPA', default=0)
    enter_year = models.IntegerField(verbose_name="Enter Year",default=0)
    major = models.CharField(verbose_name="Major",default='')

class ProfessorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_no = models.CharField(verbose_name="National Number", max_length=10, unique=True, blank=False)
    students = models.ManyToManyField('StudentProfile', through='StudentProfessor', related_name='professors', default=None)
    profile_picture = models.ImageField(upload_to='profile_pictures/', verbose_name="Profile Picture", blank=True, null=True)
    university = models.CharField(verbose_name='University', max_length=20, default='')
    college = models.CharField(verbose_name='College', max_length=20, default='')
    about_me = models.TextField(verbose_name='About Me', default='')
    def __str__(self):
        return f"{self.user} - {self.national_no}"

#intermediary model for adding some elemnts like datetime for relations if necessary
class StudentProfessor(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, default=None)
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.CASCADE, default=None)

class ProfessorFiles(models.Model):
    professor_profile = models.ForeignKey(ProfessorProfile, on_delete=models.CASCADE, related_name='files')
    uploaded_by_student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='professor_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('uploaded_by_student', 'professor_profile') 
        
#course model
def validate_zero_or_one(value):
    if value not in (0, 1):
        raise ValidationError("Value must be either 0 or 1.")

class ZeroOrOneField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [validate_zero_or_one]
        super(ZeroOrOneField, self).__init__(*args, **kwargs)
        
class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Course Name")
    term = models.IntegerField(verbose_name="Term")
    required_TAs = models.IntegerField(verbose_name="Required TAs")
    minPoint = models.IntegerField(verbose_name='minimum points')
    passCourse = ZeroOrOneField(verbose_name="should pass")
    description = models.TextField(verbose_name='description')
    professor = models.ForeignKey('ProfessorProfile', on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.name} - Term {self.term} - Section {self.professor}"


class Requests(models.Model):
    course = models.ForeignKey('Course',on_delete=models.CASCADE, related_name='course_id')
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='student_id')
    enter_year = models.IntegerField(verbose_name='sal vorodi')
    field_of_study = models.CharField(max_length=70)
    point = models.IntegerField(verbose_name='point of ta')
    gpa = models.FloatField(verbose_name='moadele daneshjo')
    status = models.CharField(max_length=10, choices=[('accept', 'Accept'), ('decline', 'Decline'), ('uncertain', 'Uncertain')])


    def __str__(self):
        return f"{self.course.name} and {self.student.user.username}"


