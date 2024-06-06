from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from django.contrib.auth.models import User
from users.models import ProfessorProfile, StudentProfile
from users.serializers import ProfessorRegisterSerializer, StudentRegisterSerializer
from django.urls import reverse
from rest_framework import status
from .models import Course
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
# class ProfessorRegistrationTest(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.user_data = {
#             "user": {
#                 "username": "testuser",
#                 "first_name": "yechi",
#                 "last_name": "yechi_dige",
#                 "email": "test@example.com",
#                 "password": "testpassword",
#             },
#             "national_no": "1222334455",
#             "password2": "testpassword",
#         }

#     def test_professor_registration(self):
#         # Create a request object
#         request = self.factory.post('/users/professor-register/', self.user_data, format='json')
        
#         # Instantiate the serializer with the request object in its context
#         serializer = ProfessorRegisterSerializer(data=self.user_data, context={'request': request})
        
#         # Check if the serializer is valid
#         if not serializer.is_valid():
#             print(serializer.errors) # Log the errors for debugging
#             self.fail("Serializer is not valid")
        
#         # Save the serializer, which should create a ProfessorProfile instance
#         serializer.save()
        
#         # Check if a ProfessorProfile instance was created
#         self.assertEqual(ProfessorProfile.objects.count(), 1)
        
#         # Check if the ProfessorProfile instance has the correct national_no
#         self.assertEqual(ProfessorProfile.objects.get().national_no, '1222334455')


# class ProfessorProfileLoginTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         # Create a User instance
#         self.user = User.objects.create_user(
#             username="testuser",
#             first_name="yechi",
#             last_name="yechi_dige",
#             email="test@example.com",
#             password="testpassword"
#         )
#         # Create a ProfessorProfile instance associated with the user
#         self.professor_profile = ProfessorProfile.objects.create(
#             user=self.user,
#             national_no="1222334455",
#         )
#         self.login_data = {
#             "username": "testuser",
#             "password": "testpassword",
#         }

#     def test_professor_login(self):
#         response = self.client.post('/users/professor-login/', self.login_data, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('token', response.data)

# # DO NOT remove this
# # class ProfessorProfileLogoutTest(TestCase):
# #     def setUp(self):
# #         self.client = APIClient()
# #         # Create a User instance
# #         self.user = User.objects.create_user(
# #             username="testuser",
# #             first_name="yechi",
# #             last_name="yechi_dige",
# #             email="test@example.com",
# #             password="testpassword"
# #         )
# #         # Create a ProfessorProfile instance associated with the user
# #         self.professor_profile = ProfessorProfile.objects.create(
# #             user=self.user,
# #             national_no="1222334455"
# #         )
# #         # Log in the user
# #         self.client.login(username="testuser", password="testpassword")

# #     def test_professor_logout(self):
# #         # Perform an action as the logged-in user
# #         # For example, accessing a protected view
# #         response = self.client.get('/users/protected-view/')
# #         self.assertEqual(response.status_code, 200)

# #         # Log out the user
# #         self.client.logout()

# #         # Verify the user is logged out by attempting to access the same view
# #         response = self.client.get('/users/protected-view/')
# #         self.assertEqual(response.status_code, 403) # Assuming the view requires authentication

# class StudentRegistrationTest(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.user_data = {
#             "user": {
#                 "username": "testuser",
#                 "first_name": "yechi",
#                 "last_name": "yechi_dige",
#                 "email": "test@example.com",
#                 "password": "testpassword",
#             },
#             "stu_no": "1222334455",
#             "phone_no": "886454665",
#             "is_ta": False,
#             "password2": "testpassword",
#         }

#     def test_Student_registration(self):
#         # Create a request object
#         request = self.factory.post('/users/student-register/', self.user_data, format='json')
        
#         # Instantiate the serializer with the request object in its context
#         serializer = StudentRegisterSerializer(data=self.user_data, context={'request': request})
        
#         # Check if the serializer is valid
#         if not serializer.is_valid():
#             print(serializer.errors) # Log the errors for debugging
#             self.fail("Serializer is not valid")
        
#         # Save the serializer, which should create a ProfessorProfile instance
#         serializer.save()
        
#         # Check if a ProfessorProfile instance was created
#         self.assertEqual(StudentProfile.objects.count(), 1)
        
#         # # Check if the ProfessorProfile instance has the correct national_no
#         # self.assertEqual(StudentProfile.objects.get().national_no, '1222334455')


# class StudentProfileLoginTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         # Create a User instance
#         self.user = User.objects.create_user(
#             username="testuser",
#             first_name="yechi",
#             last_name="yechi_dige",
#             email="test@example.com",
#             password="testpassword"
#         )
#         # Create a ProfessorProfile instance associated with the user
#         self.student_profile = StudentProfile.objects.create(
#             user=self.user,
#             stu_no = "1222334455",
#             phone_no =  "886454665",
#             is_ta = False,
#         )
#         self.login_data = {
#             "username": "testuser",
#             "password": "testpassword",
#         }

#     def test_Student_login(self):
#         response = self.client.post('/users/student-login/', self.login_data, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('token', response.data)


# class ProfessorCourseAPITest(APITestCase):
#     def test_get_courses_by_professor_name(self):
#         professor_name = 'mohammadMahdi'  # Replace with your desired professor name

#         # Create test data
#         professor_profile = ProfessorProfile.objects.create(user=User.objects.create(username=professor_name))
#         Course.objects.create(
#             name="data structure",
#             term=4022,
#             required_TAs=5,
#             num_applicants=10,
#             num_tas=3,
#             section=2,
#             professor=professor_profile
#         )

#         # Test API endpoint
#         url = reverse('professor-lesson', kwargs={'professor_name': professor_name})
#         response = self.client.get(url)

#         # Check response status code
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check response data
#         expected_data = [
#             {
#                 "id": 1,
#                 "name": "data structure",
#                 "term": 4022,
#                 "required_TAs": 5,
#                 "num_applicants": 10,
#                 "num_tas": 3,
#                 "section": 2,
#                 "professor": professor_profile.id  # Assuming ProfessorProfile has an auto-incremented id
#             }
#         ]
#         self.assertEqual(response.data, expected_data)

# class UserProfileUpdateTest(APITestCase):
#     def setUp(self):
#         # Create a user and professor profile for testing
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.professor_profile = ProfessorProfile.objects.create(user=self.user, national_no='1234567890')

#     def test_update_user_and_professor_profile(self):
#         """
#         Ensure we can update both the user and professor profile.
#         """
#         # Authenticate the request
#         self.client.force_authenticate(user=self.user)

#         # Prepare the data to be sent in the request
#         data = {
#             'user': {
#                 'email': 'newemail@example.com',
#                 'password': 'newpassword'
#             },
#             'professor_profile': {
#                 'national_no': '9876543210'
#             }
#         }

#         # Send the PATCH request
#         response = self.client.patch(reverse('profile_update'), data=data, format='json')

#         # Assert that the user and professor profile were updated
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['user']['email'], 'newemail@example.com')
#         self.assertEqual(response.data['professor_profile']['national_no'], '9876543210')
import json
from django.test import TestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from.models import ProfessorFiles, StudentProfile, ProfessorProfile

class FileUploadViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.student_user = User.objects.create_user(username='teststudent', password='testpassword')
        self.professor_user = User.objects.create_user(username='testprofessor', password='testpassword')

        # Create profiles
        self.student_profile = StudentProfile.objects.create(user=self.student_user)
        self.professor_profile = ProfessorProfile.objects.create(user=self.professor_user)

        # Set up file path
        self.file_path = 'C:\\Users\\User\\Desktop\\micro\\How to interfac.pdf'  # Ensure this path is accessible

        # Authenticate the client with the student user
        self.client.force_authenticate(user=self.student_user)
        self.token = Token.objects.create(user=self.student_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def assert_response_status_and_print_error(self, response, expected_status_code):
        print(f"\n*************MESSAGE:*******************\nResponse Error: {json.dumps(response.data)}\n")
        self.assertEqual(response.status_code, expected_status_code)
        # if response.status_code!= 200:
        #     print(f"\n*************ERROR MESSAGE:*******************\nResponse Error: {json.dumps(response.data)}\n")
        #     pass

    def test_create_new_file_upload(self):
        file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        professor_id = self.professor_profile.id
        student_id = self.student_profile.id
        response = self.client.post(reverse('file-upload', kwargs={'professor_id': professor_id}), {
            'uploaded_by_student': self.student_profile.id,
            # 'professor_profile': self.professor_profile.id,
            'file': file
        })
        self.assert_response_status_and_print_error(response, 200)
        self.assertTrue(ProfessorFiles.objects.filter(uploaded_by_student=self.student_profile).exists())

    def test_update_existing_file_upload(self):
        file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        professor_files = ProfessorFiles.objects.create(uploaded_by_student=self.student_profile, professor_profile=self.professor_profile, file=self.file_path)
        professor_id = self.professor_profile.id
        response = self.client.post(reverse('file-upload', kwargs={'professor_id': professor_id}), {
            'uploaded_by_student': self.student_profile.id,
            # 'professor_profile': self.professor_profile.id,
            'file': file,
            # 'HTTP_X_REQUEST_ID': str(professor_files.id)
        }, HTTP_AUTHORIZATION=f"Token {self.token}")
        self.assert_response_status_and_print_error(response, 200)
        self.assertEqual(ProfessorFiles.objects.get(id=professor_files.id).file, file)

    def test_invalid_request(self):
        """Test handling invalid requests."""
        professor_id = self.professor_profile.id  # Make sure to get the professor_id
        response = self.client.post(reverse('file-upload', kwargs={'professor_id': professor_id}), {
            'uploaded_by_student': 'dfs',
            'file':25,
            })
        self.assert_response_status_and_print_error(response, 400)
        self.assertIn("file", response.data)

    # def test_unauthorized_access(self):
    #     """Test unauthorized access."""
    #     response = self.client.post(reverse('file-upload', kwargs={'professor_id': self.professor_profile.id}))
    #     self.assert_response_status_and_print_error(response, 403)



