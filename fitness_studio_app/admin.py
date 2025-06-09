from django.contrib import admin
from .models import  FitnessClass,Instructor,Client

# Register your models here.
admin.site.register(FitnessClass)
admin.site.register(Instructor)     
admin.site.register(Client)
