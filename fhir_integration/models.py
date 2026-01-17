"""
FHIR (Fast Healthcare Interoperability Resources) integration
Provides standardized healthcare data exchange
"""
from django.db import models
from patients.models import Patient


class FHIRResource(models.Model):
    """
    Store FHIR resources for interoperability
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='fhir_resources',
        null=True,
        blank=True
    )
    
    resource_type = models.CharField(
        max_length=50,
        choices=[
            ('Patient', 'Patient'),
            ('Observation', 'Observation'),
            ('Condition', 'Condition'),
            ('Procedure', 'Procedure'),
            ('MedicationRequest', 'Medication Request'),
            ('DiagnosticReport', 'Diagnostic Report'),
            ('Encounter', 'Encounter'),
            ('AllergyIntolerance', 'Allergy Intolerance'),
            ('Immunization', 'Immunization'),
        ]
    )
    
    # FHIR resource ID
    fhir_id = models.CharField(max_length=255, unique=True, db_index=True)
    
    # JSON representation of FHIR resource
    resource_data = models.JSONField()
    
    # Metadata
    version = models.IntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('retired', 'Retired'),
            ('unknown', 'Unknown'),
        ],
        default='active'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # External system tracking
    external_system = models.CharField(max_length=200, blank=True)
    external_id = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['resource_type', 'fhir_id']),
            models.Index(fields=['patient']),
        ]
    
    def __str__(self):
        return f"FHIR {self.resource_type} - {self.fhir_id}"


class FHIRSync(models.Model):
    """
    Track synchronization with external FHIR servers
    """
    server_url = models.URLField()
    resource_type = models.CharField(max_length=50)
    
    sync_type = models.CharField(
        max_length=20,
        choices=[
            ('import', 'Import'),
            ('export', 'Export'),
            ('bidirectional', 'Bidirectional'),
        ]
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    
    # Sync statistics
    records_processed = models.IntegerField(default=0)
    records_success = models.IntegerField(default=0)
    records_failed = models.IntegerField(default=0)
    
    # Error tracking
    error_message = models.TextField(blank=True)
    error_details = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"FHIR Sync - {self.resource_type} - {self.status}"


class FHIRMapping(models.Model):
    """
    Map internal data models to FHIR resources
    """
    internal_model = models.CharField(max_length=100)
    internal_field = models.CharField(max_length=100)
    
    fhir_resource = models.CharField(max_length=50)
    fhir_path = models.CharField(max_length=255)
    
    # Transformation rules
    transformation_rule = models.TextField(
        blank=True,
        help_text="Python code or rule for data transformation"
    )
    
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['internal_model', 'internal_field', 'fhir_resource']
    
    def __str__(self):
        return f"{self.internal_model}.{self.internal_field} -> {self.fhir_resource}.{self.fhir_path}"
