from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import BaseUserManager

def get_current_time():
    return timezone.now().time()

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, address, age,password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
            
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, address=address, age = age, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, address, age, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user( email, username, address, age,password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',  'address', 'age']
    
    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

class Teacher_Free_Time(models.Model):
    id_teacher_free_time = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=get_current_time) 

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"Teacher Free Time : {self.name} - {self.id_teacher_free_time}"
    
class Teacher_Subject(models.Model):
    id_teacher_subject = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Teacher_Subject {self.name} {self.id_teacher_subject}"
    
class Scheduler_Subject(models.Model):
    id_scheduler_subject = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Scheduler_Subject : {self.name} - {self.id_scheduler_subject}"

class Subject(models.Model):
    id_subject = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    practice = models.IntegerField(default=0)
    theory = models.IntegerField(default=0)
    teacher_subject = models.ManyToManyField(Teacher_Subject, blank=True)
    scheduler_subject = models.ManyToManyField(Scheduler_Subject, blank=True)
    study_resolutely = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='Subject_study_resolutely')
    is_complete = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Subject : {self.name} - {self.id_subject}"
    
class Scheduler_Room(models.Model):
    id_scheduler_room = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Scheduler_Room : {self.name} - {self.id_scheduler_room}"

class Scheduler(models.Model):
    id_scheduler = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=get_current_time)
    scheduler_subject = models.ManyToManyField(Scheduler_Subject, blank=True)
    scheduler_room = models.ManyToManyField(Scheduler_Room, blank=True)
    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"Scheduler {self.name} - {self.id_scheduler}"
    
class Room(models.Model):
    id_room = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    equipment = models.CharField(max_length=255, blank=True, null=True, default='No Data')
    is_practice = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    scheduler_room = models.ManyToManyField(Scheduler_Room, blank=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Room : {self.name} - {self.id_room}"
    
class Teacher(models.Model):
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='teacher'
    )
    role = models.IntegerField(default=1)
    department = models.CharField(max_length=255, blank=True, null=True, default='No Data')
    teacher_free_time = models.ManyToManyField(Teacher_Free_Time, blank=True)
    teacher_subject = models.ManyToManyField(Teacher_Subject, blank=True)
    scheduler = models.ManyToManyField(Scheduler, blank=True)
    
    class Meta:
        ordering = ['department']

    def __str__(self):
        return f"{self.user_id.username}'s Teacher Profile"
    

