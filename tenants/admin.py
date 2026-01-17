"""
Admin configuration for Tenant management
"""
from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Tenant, Domain


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'schema_name', 'organization_type', 'is_active', 'created_on']
    list_filter = ['organization_type', 'is_active', 'subscription_tier']
    search_fields = ['name', 'schema_name', 'email']
    readonly_fields = ['created_on']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tenant', 'is_primary']
    list_filter = ['is_primary']
    search_fields = ['domain', 'tenant__name']
