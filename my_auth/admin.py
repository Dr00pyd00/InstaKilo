from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class MyuserAdmin(UserAdmin):
    list_display = ['username', 'email']
    ordering = ['username']

admin.site.register(CustomUser, MyuserAdmin)

