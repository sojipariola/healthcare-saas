"""
Admin configuration for FHIR Integration
"""
from django.contrib import admin
from .models import FHIRResource, FHIRSync, FHIRMapping


@admin.register(FHIRResource)
class FHIRResourceAdmin(admin.ModelAdmin):
    list_display = ['fhir_id', 'resource_type', 'patient', 'status', 'version', 'updated_at']
    list_filter = ['resource_type', 'status', 'updated_at']
    search_fields = ['fhir_id', 'patient__patient_id', 'external_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FHIRSync)
class FHIRSyncAdmin(admin.ModelAdmin):
    list_display = ['resource_type', 'sync_type', 'status', 'records_processed', 'records_success', 'records_failed']
    list_filter = ['status', 'sync_type', 'resource_type']
    readonly_fields = ['started_at', 'completed_at', 'created_at']


@admin.register(FHIRMapping)
class FHIRMappingAdmin(admin.ModelAdmin):
    list_display = ['internal_model', 'internal_field', 'fhir_resource', 'fhir_path', 'is_required', 'is_active']
    list_filter = ['is_required', 'is_active', 'fhir_resource']
    search_fields = ['internal_model', 'internal_field', 'fhir_resource']
