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

# class FileUploadViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#         # Create users
#         self.student_user = User.objects.create_user(username='teststudent', password='testpassword')
#         self.professor_user = User.objects.create_user(username='testprofessor', password='testpassword')

#         # Create profiles
#         self.student_profile = StudentProfile.objects.create(user=self.student_user)
#         self.professor_profile = ProfessorProfile.objects.create(user=self.professor_user)

#         # Set up file path
#         self.file_path = 'C:\\Users\\User\\Desktop\\micro\\How to interfac.pdf'  # Ensure this path is accessible

#         # Authenticate the client with the student user
#         self.client.force_authenticate(user=self.student_user)
#         # self.token = Token.objects.create(user=self.student_user)
#         # self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

#     def assert_response_status_and_print_error(self, response, expected_status_code,comment):
#         print(f"\n*************MESSAGE of {comment}:*******************\nResponse Error: {json.dumps(response.data)}\n")
#         self.assertEqual(response.status_code, expected_status_code)
#         # if response.status_code!= 200:
#         #     print(f"\n*************ERROR MESSAGE:*******************\nResponse Error: {json.dumps(response.data)}\n")
#         #     pass

#     def test_create_new_file_upload(self):
#         file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
#         professor_id = self.professor_profile.id
#         student_id = self.student_profile.id
#         response = self.client.post(reverse('file-upload', kwargs={'professor_id': professor_id}), {
#             'uploaded_by_student': self.student_profile.id,
#             # 'professor_profile': self.professor_profile.id,
#             'file': file
#         })
#         self.assert_response_status_and_print_error(response, 200,"create new")
#         self.assertTrue(ProfessorFiles.objects.filter(uploaded_by_student=self.student_profile).exists())

#     def test_update_existing_file_upload(self):
#         file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
#         professor_files = ProfessorFiles.objects.create(uploaded_by_student=self.student_profile, professor_profile=self.professor_profile, file=self.file_path)
#         professor_id = self.professor_profile.id
#         response = self.client.post(reverse('file-upload', kwargs={'professor_id': professor_id}), {
#             'uploaded_by_student': self.student_profile.id,
#             'professor_profile': self.professor_profile.id,
#             'file': file,
#             # 'HTTP_X_REQUEST_ID': str(professor_files.id)
#         })
#         self.assert_response_status_and_print_error(response, 200,"update")
#         # self.assertEqual(ProfessorFiles.objects.get(id=professor_files.id).file, file)
#         updated_file = ProfessorFiles.objects.get(id=professor_files.id)
    
#          # Now you can safely perform your assertions
#         self.assertIsNotNone(updated_file)

#     def test_invalid_request(self):
#         """Test handling invalid requests."""
#         professor_id = self.professor_profile.id  # Make sure to get the professor_id
#         response = self.client.post(reverse('file-upload', kwargs={'professor_id': professor_id}), {
#             'uploaded_by_student': 'dfs',
#             'file':25,
#             })
#         self.assert_response_status_and_print_error(response, 400,"invalid")
#         self.assertIn("file", response.data)

#     def test_post_and_get_pdf_file(self):
#         """
#         Test posting a PDF file to a professor and then retrieving it.
#         """
#         professor_id = self.professor_profile.id
        
#         # Prepare the file data for the POST request using SimpleUploadedFile
#         file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        
#         # Reverse the URL for the file upload view, passing the professor_id as a keyword argument
#         url = reverse('file-upload', kwargs={'professor_id': professor_id})
        
#         # Perform the POST request to upload the file
#         response = self.client.post(url, {'file': file}, format='multipart')
        
#         # Assert that the POST request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(ProfessorFiles.objects.exists())
        
#         # Extract the ID of the newly created file
#         file_id = ProfessorFiles.objects.first().id
        
#         # Prepare the URL for the GET request, using the file ID
#         get_url = reverse('file-upload', kwargs={'file_id': file_id})  # Adjust 'file-retrieve' to match your URL pattern name
        
#         # Perform the GET request to retrieve the file
#         get_response = self.client.get(get_url)
        
#         # Assert that the GET request was successful and the file data is returned
#         self.assertEqual(get_response.status_code, status.HTTP_200_OK)
#         self.assertIn('url', get_response.data)
#     # def test_unauthorized_access(self):
#     #     """Test unauthorized access."""
#     #     response = self.client.post(reverse('file-upload', kwargs={'professor_id': self.professor_profile.id}))
#     #     self.assert_response_status_and_print_error(response, 403)

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from.models import ProfessorFiles, ProfessorProfile, StudentProfile

class GetFileURLViewTest(TestCase):
    def setUp(self):
        # Create a professor user and profile
        self.professor_user = User.objects.create_user(username='professor', password='password123')
        self.professor_profile = ProfessorProfile.objects.create(user=self.professor_user)

        # Create a student user and profile
        self.student_user = User.objects.create_user(username='student', password='password456')
        self.student_profile = StudentProfile.objects.create(user=self.student_user)

        # Create a file instance
        self.file_instance = ProfessorFiles.objects.create(
            professor_profile=self.professor_profile,
            uploaded_by_student=self.student_profile,
            file='dummy/file/path.pdf',
            uploaded_at='2024-01-01T00:00:00Z'
        )

        # Instantiate the test client
        self.client = Client()

    def test_get_file_url_success(self):
        # Authenticate as the professor
        self.client.login(username='professor', password='password123')

        # Construct the URL for the view, including the student's ID
        url = reverse('get-file-url', args=[self.student_profile.id])

        # Make the GET request to the view
        response = self.client.get(url)

        # Check that the response has a 200 OK status code
        self.assertEqual(response.status_code, 200)

        # Check that the response data includes the file URL
        self.assertIn('file_url', response.json())
        expected_file_url = '/media/dummy/file/path.pdf'  # Adjust based on your MEDIA_URL setting
        self.assertEqual(response.json()['file_url'], expected_file_url)

    def test_get_file_url_failure_no_file(self):
        # Remove the file instance to simulate a scenario where no file exists
        self.file_instance.delete()

        # Authenticate as the professor
        self.client.login(username='professor', password='password123')

        # Construct the URL for the view, including the student's ID
        url = reverse('get-file-url', args=[self.student_profile.id])

        # Make the GET request to the view
        response = self.client.get(url)

        # Check that the response has a 404 Not Found status code
        self.assertEqual(response.status_code, 404)

        # Check that the response data includes an error message
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], "No file found for this professor and student combination.")


