
from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ("id", "username", "email", "tenant", "role", "is_active", "is_staff")
	search_fields = ("username", "email", "tenant__name", "role")
