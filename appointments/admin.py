
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	list_display = ("id", "patient", "scheduled_for", "status", "created_at")
	search_fields = ("patient__first_name", "patient__last_name", "status")
