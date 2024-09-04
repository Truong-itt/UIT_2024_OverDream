from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Teacher_Free_Time)
admin.site.register(Teacher_Subject)
admin.site.register(Scheduler)  
admin.site.register(Subject) 
admin.site.register(Room) 
admin.site.register(Scheduler_Room) 
admin.site.register(Scheduler_Subject) 
