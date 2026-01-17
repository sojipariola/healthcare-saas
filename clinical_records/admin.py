"""
Admin configuration for Clinical Records
"""
from django.contrib import admin
from .models import ClinicalRecord, Prescription, LabResult, ImagingStudy


@admin.register(ClinicalRecord)
class ClinicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'provider', 'encounter_date', 'is_finalized']
    list_filter = ['is_finalized', 'encounter_date']
    search_fields = ['patient__patient_id', 'provider__username']
    readonly_fields = ['created_at', 'updated_at', 'finalized_at']
    date_hierarchy = 'encounter_date'


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'medication_name', 'prescribed_by', 'status', 'prescribed_date']
    list_filter = ['status', 'prescribed_date']
    search_fields = ['patient__patient_id', 'medication_name']
    readonly_fields = ['prescribed_date']


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ['patient', 'test_name', 'status', 'ordered_by', 'ordered_date']
    list_filter = ['status', 'is_abnormal', 'ordered_date']
    search_fields = ['patient__patient_id', 'test_name']


@admin.register(ImagingStudy)
class ImagingStudyAdmin(admin.ModelAdmin):
    list_display = ['patient', 'study_type', 'body_part', 'status', 'ordered_date']
    list_filter = ['study_type', 'status', 'ordered_date']
    search_fields = ['patient__patient_id', 'body_part']
