from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView 
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .serializers import *
from rest_framework.authtoken.models import Token
from .models import ProfessorProfile, StudentProfile
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import UserPassesTestMixin
import operator
from functools import reduce
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import os
from rest_framework.parsers import MultiPartParser, FormParser

class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset() 
        queryset = self.filter_queryset(queryset)  
        filters = {}
        pk_fields = ["pk", "id"]
        for field in self.lookup_fields:
            identifier = self.kwargs[self.lookup_field]
            if (field in pk_fields and identifier.isdigit()) or field not in pk_fields:
                filters[field] = self.kwargs[self.lookup_field]
        q = reduce(operator.or_, (Q(x) for x in filters.items()))
        obj = get_object_or_404(queryset, q)
        self.check_object_permissions(self.request, obj)
        return obj


class ProfessorRegisterView(GenericAPIView):
    serializer_class = ProfessorRegisterSerializer
    def post(self, request):
        serializer = ProfessorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response("professor successfully registered!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            try:
                student = StudentProfile.objects.get(user=user)
            except ObjectDoesNotExist:
                student = None
                professor = ProfessorProfile.objects.get(user=user)
            if student != None:
                user_data = {
                    'id': user.id,
                    'role': "student",
                    'studentid': student.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    "last_name": user.last_name,
                    'phone_no': student.phone_no,
                    'stu_no': student.stu_no,
                    'is_ta': student.is_ta,
                    'email': user.email,
                    'university': student.university,
                    'college': student.college,
                    'about_me': student.about_me,
                    'gpa': student.gpa,
                    'enter_year': student.enter_year,
                    'major': student.major,
                    'average': student.average,
                }
                return Response({"token": token.key, "user_data": user_data}, status=status.HTTP_200_OK)
            else:
                user_data = {
                'professorid':professor.id,
                'id': user.id,
                'role': "professor",
                'username': user.username,
                'first_name': user.first_name,
                "last_name": user.last_name,
                'national_no': professor.national_no,
                'email': user.email,
                'university': professor.university,
                'college': professor.college,
                'about_me': professor.about_me,
                }
                return Response({"token": token.key, "user_data": user_data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentRegisterView(GenericAPIView):
    serializer_class = StudentRegisterSerializer
    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response("student successfully registered!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permissions_classes = [IsAuthenticated]
    serializer_class = RequestsSerializer
    def get(self, request, role, id):
        if role == 'student':
            try:
                ret_data = Requests.objects.filter(student=id)
            except:
                return Response(data="student not found",status=status.HTTP_404_NOT_FOUND)

        if role == 'professor':
            try:
                ret_data = Requests.objects.filter(course__professor=id)
            except:
                return Response(data="professor not found", status=status.HTTP_404_NOT_FOUND)

        serializer = RequestsSerializer(ret_data, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, role, id):
        serializer = RequestsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, role, id):
        pk = request.data.get('id')
        req = get_object_or_404(Requests, pk=pk)
        serializer = RequestsSerializer(instance=req, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)



class ProfessorCourseAPIView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    def get(self, request, name):

        try:
            users = User.objects.get(username=name)
            professor = ProfessorProfile.objects.get(user=users)

        except ProfessorProfile.DoesNotExist:
            return Response("Professor not found(course api)", status=status.HTTP_404_NOT_FOUND)

        courses = professor.courses.all()

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self,request,name):
        serialize = CourseSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteCourse(request, name, id):
    cousre = Course.objects.get(id=id)
    cousre.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def allCourseInStudent(request):
    courses = Course.objects.all()
    serializer = CourseForHomeStudentSerializer(courses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




class CourseRegisterView(GenericAPIView):
    serializer_class = CourseSerializer
    def post(self, request):
        name = request.data.get('name')
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(f"lesson '{name}' is added to database", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfessorDetailsView(UserPassesTestMixin, GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def test_func(self):
        user_id = self.kwargs['professor_id'] 
        try:
            professor = ProfessorProfile.objects.get(user__id=user_id)
            return True 
        except ProfessorProfile.DoesNotExist:
            return False

    def get(self, request, professor_id):
        try:
            professor = ProfessorProfile.objects.get(user=request.user)
        except ProfessorProfile.DoesNotExist:
            return Response({"error": "Professor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        students = StudentProfile.objects.filter(studentprofessor__professor=professor)
        
        
        professor_serializer = ProfessorProfileSerializer(professor)
        students_serializer = StudentProfileSerializer(students, many=True)
        
       
        data = {
            "professor": professor_serializer.data,
            "students": students_serializer.data
        }
        
        return Response(data, status=status.HTTP_200_OK)

class UserPartialUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  

class StudentProfilePartialUpdateView(generics.UpdateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.phone_no = request.data.get('phone_no', instance.phone_no)
        instance.is_ta = request.data.get('is_ta', instance.is_ta)  
        instance.university = request.data.get('university', instance.university)
        instance.college = request.data.get('college', instance.college)
        instance.about_me = request.data.get('about_me', instance.about_me)
        instance.gpa = request.data.get('gpa', instance.gpa)
        instance.enter_year = request.data.get('enter_year', instance.enter_year)
        instance.major = request.data.get('major', instance.major)
        instance.save(update_fields=['phone_no', 'is_ta','university','college','about_me','gpa','enter_year','major'])  
        return super().partial_update(request, *args, **kwargs)

class ProfessorProfilePartialUpdateView(generics.UpdateAPIView):
    queryset = ProfessorProfile.objects.all()
    serializer_class = ProfessorProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id' 

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.national_no = request.data.get('national_no', instance.national_no)
        instance.university = request.data.get('university', instance.university)
        instance.college = request.data.get('college', instance.college)
        instance.about_me = request.data.get('about_me', instance.about_me)
        instance.save(update_fields=['national_no','university','college','about_me'])
        return super().partial_update(request, *args, **kwargs)

class CourseDeleteView(MultipleFieldLookupMixin, generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name' 
    lookup_fields = ('name', 'id')  


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def student_profile_picture(request):
    if request.method == 'GET':
        try:
            profile = StudentProfile.objects.get(user=request.user)
            serializer = StudentProfileSerializer(profile)
            return Response(serializer.data['profile_picture'])
        except StudentProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method in ['PUT', 'PATCH']:
        parser_classes = (MultiPartParser, FormParser,)
        profile = StudentProfile.objects.get(user=request.user)
        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def professor_profile_picture(request):
    if request.method == 'GET':
        try:
            profile = ProfessorProfile.objects.get(user=request.user)
            serializer = ProfessorProfileSerializer(profile)
            return Response(serializer.data['profile_picture'])
        except ProfessorProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method in ['PUT', 'PATCH']:
        parser_classes = (MultiPartParser, FormParser,)
        profile = ProfessorProfile.objects.get(user=request.user)
        serializer = ProfessorProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def update_student_rate(request):
    serializer = RateSerializer(data=request.data)
    if serializer.is_valid():
        student_id = serializer.validated_data['id']
        rate = serializer.validated_data['rate']

        professor_profile = None
        try:
            professor_profile = ProfessorProfile.objects.get(user=request.user)
        except ProfessorProfile.DoesNotExist:
            return Response({"error": "User is not a professor."}, status=403)

        try:
            student_profile = StudentProfile.objects.get(user__id=student_id)
            student_profile.rate_sum += rate
            student_profile.rate_count += 1
            student_profile.average = student_profile.rate_sum // student_profile.rate_count
            student_profile.save()

            return Response({"average": student_profile.average}, status=status.HTTP_200_OK)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FileUploadSerializer
    def post(self, request, professor_id, *args, **kwargs):
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            professor_profile = ProfessorProfile.objects.get(id=professor_id)
        except (StudentProfile.DoesNotExist, ProfessorProfile.DoesNotExist):
            return Response({"error": "Invalid user or professor ID."}, status=status.HTTP_400_BAD_REQUEST)

        existing_file = ProfessorFiles.objects.filter(uploaded_by_student=student_profile, professor_profile=professor_profile).first()
        
        serializer = FileUploadSerializer(data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            if existing_file:
                # Update the existing instance
                serializer.update(existing_file, serializer.validated_data)
            else:
                # Create a new instance
                serializer.save(uploaded_by_student=student_profile, professor_profile=professor_profile)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

