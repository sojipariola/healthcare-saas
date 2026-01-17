"""
Immutable audit logging system for HIPAA compliance
All actions on sensitive data are logged and cannot be modified
"""
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import json


class AuditLog(models.Model):
    """
    Immutable audit log entry
    All access to PHI and system actions are logged
    """
    # User information
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    username = models.CharField(max_length=150)  # Store username in case user is deleted
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Action details
    action = models.CharField(
        max_length=50,
        choices=[
            ('create', 'Create'),
            ('read', 'Read/View'),
            ('update', 'Update'),
            ('delete', 'Delete'),
            ('login', 'Login'),
            ('logout', 'Logout'),
            ('failed_login', 'Failed Login'),
            ('export', 'Export Data'),
            ('print', 'Print'),
            ('search', 'Search'),
        ]
    )
    
    # Resource being accessed
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.CharField(max_length=255, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional context
    resource_type = models.CharField(max_length=100)  # e.g., "Patient", "ClinicalRecord"
    resource_id = models.CharField(max_length=255)  # Store ID even if object is deleted
    
    # Change details
    changes = models.JSONField(default=dict, blank=True)
    previous_values = models.JSONField(default=dict, blank=True)
    new_values = models.JSONField(default=dict, blank=True)
    
    # Request metadata
    request_method = models.CharField(max_length=10, blank=True)
    request_path = models.CharField(max_length=500, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    # Compliance fields
    reason_for_access = models.TextField(blank=True, help_text="Why was this data accessed?")
    
    # Timestamp (immutable)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Session tracking
    session_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['resource_type', 'resource_id']),
            models.Index(fields=['timestamp']),
        ]
        # Make the model immutable after creation
        permissions = [
            ("access_auditlog", "Can access audit logs"),
            # Note: No add, change, or delete permissions should be granted
        ]
    
    def __str__(self):
        return f"{self.username} - {self.action} - {self.resource_type} - {self.timestamp}"
    
    def save(self, *args, **kwargs):
        """Override save to prevent updates"""
        if self.pk is not None:
            # Prevent updates to existing audit logs
            raise Exception("Audit logs are immutable and cannot be modified")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Override delete to prevent deletion"""
        raise Exception("Audit logs are immutable and cannot be deleted")


class DataAccessLog(models.Model):
    """
    Specific log for PHI data access
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    patient_id = models.CharField(max_length=50, db_index=True)
    
    access_type = models.CharField(
        max_length=50,
        choices=[
            ('view_demographics', 'View Demographics'),
            ('view_medical_history', 'View Medical History'),
            ('view_clinical_record', 'View Clinical Record'),
            ('view_prescription', 'View Prescription'),
            ('view_lab_results', 'View Lab Results'),
            ('view_imaging', 'View Imaging'),
            ('view_billing', 'View Billing'),
            ('modify', 'Modify Data'),
            ('export', 'Export Data'),
        ]
    )
    
    access_reason = models.TextField(help_text="Reason for accessing PHI")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Access context
    access_granted = models.BooleanField(default=True)
    denial_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['patient_id', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username if self.user else 'Unknown'} - {self.access_type} - Patient {self.patient_id}"
    
    def save(self, *args, **kwargs):
        """Override save to prevent updates"""
        if self.pk is not None:
            raise Exception("Data access logs are immutable and cannot be modified")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Override delete to prevent deletion"""
        raise Exception("Data access logs are immutable and cannot be deleted")


class SecurityEvent(models.Model):
    """
    Security-related events for monitoring
    """
    event_type = models.CharField(
        max_length=50,
        choices=[
            ('unauthorized_access', 'Unauthorized Access Attempt'),
            ('failed_login', 'Failed Login'),
            ('permission_denied', 'Permission Denied'),
            ('data_breach_attempt', 'Data Breach Attempt'),
            ('suspicious_activity', 'Suspicious Activity'),
            ('policy_violation', 'Policy Violation'),
        ]
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    username_attempt = models.CharField(max_length=150, blank=True)
    
    description = models.TextField()
    severity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='medium'
    )
    
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    request_path = models.CharField(max_length=500, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Response taken
    action_taken = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['severity', 'timestamp']),
            models.Index(fields=['event_type', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.severity} - {self.timestamp}"
