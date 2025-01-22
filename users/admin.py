from django.contrib import admin
from .models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['username', 'email', 'first_name', 'last_name', 'phone_number']