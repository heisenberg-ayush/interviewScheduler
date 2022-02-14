from django.contrib import admin

# Register your models here.
from .models import User, Student

admin.site.register(User)
admin.site.register(Student)