from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
User = get_user_model()

class TeacherSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['role', 'department']

class UserSerializer(serializers.ModelSerializer):
    teacher_details = TeacherSearchSerializer(source='teacher', read_only=True)
    class Meta:
        model = User
        fields = ['id_user', 'username', 'email', 'address', 'age', 'is_active', 'is_staff','create_at', 'teacher_details']

class TeacherFreeTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher_Free_Time
        fields = '__all__'

class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher_Subject
        fields = '__all__'

class SchedulerSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher_Subject
        fields = '__all__'

class SchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler_Subject
        fields = '__all__'

class SchedulerRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler_Room
        fields = '__all__'
        
class SimpleSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id_subject', 'name']
        
class SubjectSerializer(serializers.ModelSerializer):
    teacher_subject = TeacherSubjectSerializer(many=True, required=False)
    scheduler_subject = SchedulerSerializer(many=True, required=False)
    study_resolutely = SimpleSubjectSerializer(many=True, required=False)
    class Meta:
        model = Subject
        fields = ['id_subject', 'name', 'practice', 'theory', 'teacher_subject', 'scheduler_subject', 'study_resolutely', 'is_complete']
        
class TeacherSerializer(serializers.ModelSerializer):
    teacher_free_time = TeacherFreeTimeSerializer(many=True, required=False)
    teacher_subject = TeacherSubjectSerializer(many=True, required=False)
    scheduler = SchedulerSerializer(many=True, required=False)
    user_id = UserSerializer(read_only=True, required=False)
    class Meta:
        model = Teacher
        fields = ['user_id', 'role', 'department','teacher_free_time', 'teacher_subject', 'scheduler']
        
class RoomSerializer(serializers.ModelSerializer):
    scheduler_room = SchedulerRoomSerializer(many=True, required=False)
    class Meta:
        model = Room
        fields = ['id_room', 'name', 'equipment', 'is_practice', 'create_at', 'scheduler_room']
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email' , 'username', 'address', 'age', 'password')
        extra_kwargs = {'email': {'required': True}, 'password': {'required': True}}  # Đảm bảo email là bắt buộc

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError("Invalid email address")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            address = validated_data['address'],
            age = validated_data['age'],
            password=validated_data['password']
        )
        return user