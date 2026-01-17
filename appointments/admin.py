"""
Admin configuration for Appointments
"""
from django.contrib import admin
from .models import Appointment, AppointmentSlot


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'provider', 'appointment_date', 'appointment_time', 'appointment_type', 'status']
    list_filter = ['status', 'appointment_type', 'appointment_date']
    search_fields = ['patient__patient_id', 'provider__username', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'appointment_date'


@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ['provider', 'date', 'start_time', 'end_time', 'is_available']
    list_filter = ['is_available', 'provider', 'date']
    date_hierarchy = 'date'
