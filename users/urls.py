from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('professor-register/', ProfessorRegisterView.as_view(), name='professor-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('student-register/', StudentRegisterView.as_view(), name='student-register'),
    path('professor/<str:name>/lesson/', ProfessorCourseAPIView.as_view(), name= 'professor-lesson'),
    path('professor/<str:name>/lesson/<int:id>', deleteCourse , name='professor-lesson'),
    path('professor/create-lesson/', CourseRegisterView.as_view(), name= 'create-lesson'),
    path('professor/get-detail/<int:professor_id>', ProfessorDetailsView.as_view(), name='professor-details'),
    path('student/profile/<int:id>/', StudentProfilePartialUpdateView.as_view(), name='partial_update_student_profile'),
    path('professor/profile/<int:id>/', ProfessorProfilePartialUpdateView.as_view(), name='partial_update_professor_profile'),
    path('update/<int:id>/', UserPartialUpdateView.as_view(), name='user_partial_update'),
    path('professor/delete-lesson/<str:name>/', CourseDeleteView.as_view(), name='course_delete_by_name'),
    path('request/<str:role>/<int:id>', RequestView.as_view(), name='requests'),
    path('student/home/', allCourseInStudent, name='all_course'),
    path('student/profile-picture/', student_profile_picture, name='student_profile_picture'),
    path('professor/profile-picture/', professor_profile_picture, name='professor_profile_picture'),
    path('professor/update-rate/', update_student_rate, name='update_student_rate'),
    path('student/upload-resume/<int:professor_id>/', FileUploadView.as_view(), name='file-upload'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
