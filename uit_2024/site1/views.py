from django.shortcuts import render
from django.http import HttpResponse
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import Http404
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken 
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import *
from .serializers import *
import logging
logger = logging.getLogger(__name__)

# Create your views here.

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Description of your API",
      terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class UserDetailView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class TeacherView(APIView):
    def get(self, request):
        teacher = Teacher.objects.all()
        serializer = TeacherSerializer(teacher, many=True)
        return Response(serializer.data)
    
class TeacherDetailView(APIView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
    
class TeacherFreeTimeView(APIView):
    def get(self, request):
        teacher_free_time = Teacher_Free_Time.objects.all()
        serializer = TeacherFreeTimeSerializer(teacher_free_time, many=True)
        return Response(serializer.data)
    
class TeacherFreeTimeDetailView(APIView):
    def get_object(self, pk):
        try:
            return Teacher_Free_Time.objects.get(pk=pk)
        except Teacher_Free_Time.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        teacher_free_time = self.get_object(pk)
        serializer = TeacherFreeTimeSerializer(teacher_free_time)
        return Response(serializer.data)
    
class TeacherSubjectView(APIView):
    def get(self, request):
        teacher_subject = Teacher_Subject.objects.all()
        serializer = TeacherSubjectSerializer(teacher_subject, many=True)
        return Response(serializer.data)
    
class TeacherSubjectDetailView(APIView):
    def get_object(self, pk):
        try:
            return Teacher_Subject.objects.get(pk=pk)
        except Teacher_Subject.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        teacher_subject = self.get_object(pk)
        serializer = TeacherSubjectSerializer(teacher_subject)
        return Response(serializer.data)
    
class SchedulerView(APIView):
    def get(self, request):
        scheduler = Scheduler.objects.all()
        serializer = SchedulerSerializer(scheduler, many=True)
        return Response(serializer.data)
    
class SchedulerDetailView(APIView):
    def get_object(self, pk):
        try:
            return Scheduler.objects.get(pk=pk)
        except Scheduler.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        scheduler = self.get_object(pk)
        serializer = SchedulerSerializer(scheduler)
        return Response(serializer.data)
    
class SchedulerSubjectView(APIView):
    def get(self, request):
        scheduler_subject = Scheduler_Subject.objects.all()
        serializer = SchedulerSubjectSerializer(scheduler_subject, many=True)
        return Response(serializer.data)
    
class SchedulerSubjectDetailView(APIView):
    def get_object(self, pk):
        try:
            return Scheduler_Subject.objects.get(pk=pk)
        except Scheduler_Subject.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        scheduler_subject = self.get_object(pk)
        serializer = SchedulerSubjectSerializer(scheduler_subject)
        return Response(serializer.data)
    
class SchedulerRoomView(APIView):
    def get(self, request):
        scheduler_room = Scheduler_Room.objects.all()
        serializer = SchedulerRoomSerializer(scheduler_room, many=True)
        return Response(serializer.data)
    
class SchedulerRoomDetailView(APIView):
    def get_object(self, pk):
        try:
            return Scheduler_Room.objects.get(pk=pk)
        except Scheduler_Room.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        scheduler_room = self.get_object(pk)
        serializer = SchedulerRoomSerializer(scheduler_room)
        return Response(serializer.data)
    
class SubjectView(APIView):
    def get(self, request):
        subject = Subject.objects.all()
        serializer = SubjectSerializer(subject, many=True)
        return Response(serializer.data)
    
class SubjectDetailView(APIView):
    def get_object(self, pk):
        try:
            return Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        subject = self.get_object(pk)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)
    
class RoomView(APIView):
    def get(self, request):
        room = Room.objects.all()
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)

class RoomDetailView(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    
# search 
@api_view(['POST'])
def search_teacher(request):
    search_text = request.data.get('search_text', '')
    if search_text:
        users = User.objects.filter(username__icontains=search_text).select_related('teacher')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No search data provided"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST']) 
def search_room(request):
    search_text = request.data.get('search_text', '')
    if search_text:
        rooms = Room.objects.filter(name__icontains=search_text)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No search data provided"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def search_subject(request):
    search_text = request.data.get('search_text', '')
    if search_text:
        subjects = Subject.objects.filter(name__icontains=search_text)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No search data provided"}, status=status.HTTP_400_BAD_REQUEST)
    
# login/registry
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        logger.info(request.data)
        print(request.data)
        serializer = AuthTokenSerializer(data=request.data)
        print(f"thong tin serializer: {serializer}")
        print("-------------------------------")
        serializer.is_valid(raise_exception=True)
        print(f"serialize {serializer}")
        print(f"serialize {serializer.is_valid(raise_exception=True)}")
        # print(f"serialize {serializer.is_valid()}")
        user = serializer.validated_data['user']
        print(f"user {user}") 
        login(request, user)
        return super(LoginView, self).post(request, format=None)

class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            _, token = AuthToken.objects.create(user)
            data = {
                "user": UserSerializer(user).data,
                "token": token
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)