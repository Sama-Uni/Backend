from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import ProfessorProfile, StudentProfile, Course, Requests
from django.contrib.auth import authenticate
from rest_framework import generics

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
    

class ProfessorRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = ProfessorProfile
        fields = ['user', 'national_no', 'password2']

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User already exists!")
        return username

    def validate(self, data):
        if data['user']['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        national_no = validated_data.pop('national_no')
        prof = ProfessorProfile.objects.create(user=user, national_no=national_no)
        return prof

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(request=self.context.get('request'), **data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class StudentRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = StudentProfile
        fields = ['user', 'stu_no', "phone_no" , 'is_ta' , 'password2']

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User already exists!")
        return username

    def validate(self, data):
        if data['user']['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        stu_no = validated_data.pop('stu_no')
        phone_no = validated_data.pop('phone_no')
        is_ta = validated_data.pop('is_ta')
        stu = StudentProfile.objects.create(user=user, stu_no=stu_no, is_ta=is_ta, phone_no=phone_no)
        return stu

class CourseForHomeStudentSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(queryset=ProfessorProfile.objects.all())
    professorName = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ('id', 'term', 'required_TAs', 'minPoint', 'passCourse', 'description', 'professor', 'professorName', 'name')

    def get_professorName(self, obj):
        return obj.professor.user.username


class CourseSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(queryset=ProfessorProfile.objects.all())

    class Meta:
        model = Course
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['user','stu_no','is_ta','phone_no']  # Adjust this to include only the fields you want to expose

class ProfessorProfileSerializer(serializers.ModelSerializer):
    students = StudentProfileSerializer(many=True, read_only=True)

    class Meta:
        model = ProfessorProfile
        fields = ['user','national_no','students']  # Adjust this to include only the fields you want to expose


class RequestsSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Requests
        fields = '__all__'

