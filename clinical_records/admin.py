
from django.contrib import admin
from .models import ClinicalRecord

@admin.register(ClinicalRecord)
class ClinicalRecordAdmin(admin.ModelAdmin):
	list_display = ("id", "patient", "created_at")
	search_fields = ("patient__first_name", "patient__last_name")
