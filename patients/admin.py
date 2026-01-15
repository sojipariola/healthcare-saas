
from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ("id", "first_name", "last_name", "date_of_birth", "email", "phone", "created_at")
	search_fields = ("first_name", "last_name", "email", "phone")
