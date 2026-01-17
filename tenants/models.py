"""
Multi-tenant models for healthcare SaaS platform
Each tenant represents a separate healthcare organization with isolated data
"""
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    """
    Tenant model representing a healthcare organization
    Each tenant has its own database schema for data isolation
    """
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    
    # Organization details
    organization_type = models.CharField(
        max_length=50,
        choices=[
            ('hospital', 'Hospital'),
            ('clinic', 'Clinic'),
            ('private_practice', 'Private Practice'),
            ('laboratory', 'Laboratory'),
            ('pharmacy', 'Pharmacy'),
        ],
        default='clinic'
    )
    
    # Contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Compliance settings
    hipaa_compliance_enabled = models.BooleanField(default=True)
    gdpr_compliance_enabled = models.BooleanField(default=True)
    
    # Subscription and status
    is_active = models.BooleanField(default=True)
    subscription_tier = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic'),
            ('professional', 'Professional'),
            ('enterprise', 'Enterprise'),
        ],
        default='basic'
    )
    
    # Auto-generated fields from TenantMixin: schema_name, on_trial, etc.
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Domain(DomainMixin):
    """
    Domain model for tenant routing
    Maps domains/subdomains to tenants
    """
    pass
