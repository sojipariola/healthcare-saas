"""
Admin configuration for Patient management
"""
from django.contrib import admin
from .models import Patient, PatientNote


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'get_full_name', 'gender', 'date_of_birth', 'is_active', 'created_at']
    list_filter = ['is_active', 'gender', 'consent_to_treat', 'hipaa_consent']
    search_fields = ['patient_id', 'first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Identification', {
            'fields': ('patient_id', 'is_active')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'ssn')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'city', 'state', 'zip_code')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Insurance', {
            'fields': ('insurance_provider', 'insurance_policy_number', 'insurance_group_number')
        }),
        ('Medical Information', {
            'fields': ('blood_type', 'allergies', 'current_medications', 'medical_history')
        }),
        ('Consent & Compliance', {
            'fields': ('consent_to_treat', 'hipaa_consent', 'consent_date')
        }),
        ('Care Team', {
            'fields': ('primary_physician',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PatientNote)
class PatientNoteAdmin(admin.ModelAdmin):
    list_display = ['patient', 'note_type', 'created_by', 'created_at']
    list_filter = ['note_type', 'created_at']
    search_fields = ['patient__patient_id', 'title', 'content']
    readonly_fields = ['created_at', 'updated_at']
