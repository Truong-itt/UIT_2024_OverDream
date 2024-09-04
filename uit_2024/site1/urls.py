from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # user 
    path('user/', UserView.as_view(), name='get-user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='get-user'),
    # teacher 
    path('teacher/', TeacherView.as_view(), name='get-user'),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), name='get-user'),
    
    # teacher free time 
    path('teacher-free-time/', TeacherFreeTimeView.as_view(), name='get-user'),
    path('teacher-free-time/<int:pk>', TeacherFreeTimeDetailView.as_view(), name='get-user'),
    
    # teacher subject
    path('teacher-subject/', TeacherSubjectView.as_view(), name='get-user'),
    path('teacher-subject/<int:pk>', TeacherSubjectDetailView.as_view(), name='get-user'),
    
    # Scheduler 
    path('scheduler/', SchedulerView.as_view(), name='get-user'),
    path('scheduler/<int:pk>', SchedulerDetailView.as_view(), name='get-user'),
    
    
    # Scheduler subject 
    path('scheduler-subject/', SchedulerSubjectView.as_view(), name='get-user'),
    path('scheduler-subject/<int:pk>', SchedulerSubjectDetailView.as_view(), name='get-user'),
    
    # Scheduler room
    path('scheduler-room/', SchedulerRoomView.as_view(), name='get-user'),
    path('scheduler-room/<int:pk>', SchedulerRoomDetailView.as_view(), name='get-user'),
    
    # subject
    path('subject/', SubjectView.as_view(), name='get-user'),
    path('subject/<int:pk>', SubjectDetailView.as_view(), name='get-user'),
    # room 
    path('room/', RoomView.as_view(), name='get-user'),
    path('room/<int:pk>', RoomDetailView.as_view(), name='get-user'),

    # search
    path('search-teacher/', search_teacher, name='search-teacher'),
    path('search-room/', search_room, name='search-room'),
    path('search-subject/', search_subject, name='search-subject'),
    
    # login/registry/token
    path('login/', LoginView.as_view(), name='loginview'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('get-user-token/', GetUserView.as_view(), name='get-user'),
    
    
]
