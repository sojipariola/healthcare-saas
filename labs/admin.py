
from django.contrib import admin
from .models import LabResult

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
	list_display = ("id", "patient", "created_at")
	search_fields = ("patient__first_name", "patient__last_name")
