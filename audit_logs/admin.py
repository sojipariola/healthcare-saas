"""
Admin configuration for Audit Logs (Read-only)
"""
from django.contrib import admin
from .models import AuditLog, DataAccessLog, SecurityEvent


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['username', 'action', 'resource_type', 'resource_id', 'timestamp']
    list_filter = ['action', 'resource_type', 'timestamp']
    search_fields = ['username', 'resource_id', 'user_ip']
    readonly_fields = [f.name for f in AuditLog._meta.fields]
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DataAccessLog)
class DataAccessLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'patient_id', 'access_type', 'access_granted', 'timestamp']
    list_filter = ['access_type', 'access_granted', 'timestamp']
    search_fields = ['patient_id', 'user__username']
    readonly_fields = [f.name for f in DataAccessLog._meta.fields]
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'severity', 'user', 'username_attempt', 'timestamp', 'resolved']
    list_filter = ['event_type', 'severity', 'resolved', 'timestamp']
    search_fields = ['username_attempt', 'description', 'ip_address']
    readonly_fields = ['event_type', 'user', 'username_attempt', 'description', 'severity', 
                      'ip_address', 'user_agent', 'request_path', 'timestamp']
    date_hierarchy = 'timestamp'
