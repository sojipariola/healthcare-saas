"""
Patient models with encrypted PHI (Protected Health Information)
All sensitive data is encrypted at rest for HIPAA compliance
"""
from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt


class Patient(models.Model):
    """
    Patient model with encrypted PHI fields
    """
    # Non-encrypted identifiers
    patient_id = models.CharField(max_length=50, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Encrypted personal information (PHI)
    first_name = encrypt(models.CharField(max_length=100))
    last_name = encrypt(models.CharField(max_length=100))
    date_of_birth = encrypt(models.DateField())
    ssn = encrypt(models.CharField(max_length=11, blank=True))  # Social Security Number
    
    # Encrypted contact information
    email = encrypt(models.EmailField(blank=True))
    phone = encrypt(models.CharField(max_length=20, blank=True))
    address = encrypt(models.TextField(blank=True))
    city = encrypt(models.CharField(max_length=100, blank=True))
    state = encrypt(models.CharField(max_length=50, blank=True))
    zip_code = encrypt(models.CharField(max_length=10, blank=True))
    
    # Demographics
    gender = models.CharField(
        max_length=20,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not_to_say', 'Prefer not to say'),
        ],
        blank=True
    )
    
    # Encrypted emergency contact
    emergency_contact_name = encrypt(models.CharField(max_length=100, blank=True))
    emergency_contact_phone = encrypt(models.CharField(max_length=20, blank=True))
    emergency_contact_relationship = encrypt(models.CharField(max_length=50, blank=True))
    
    # Insurance information (encrypted)
    insurance_provider = encrypt(models.CharField(max_length=100, blank=True))
    insurance_policy_number = encrypt(models.CharField(max_length=100, blank=True))
    insurance_group_number = encrypt(models.CharField(max_length=100, blank=True))
    
    # Medical information
    blood_type = models.CharField(
        max_length=5,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        blank=True
    )
    
    allergies = encrypt(models.TextField(blank=True, help_text="List of known allergies"))
    current_medications = encrypt(models.TextField(blank=True))
    medical_history = encrypt(models.TextField(blank=True))
    
    # Consent and compliance
    consent_to_treat = models.BooleanField(default=False)
    hipaa_consent = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)
    
    # Assigned care provider
    primary_physician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients'
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Patient {self.patient_id}"
    
    def get_full_name(self):
        """Returns decrypted full name"""
        return f"{self.first_name} {self.last_name}"


class PatientNote(models.Model):
    """
    Clinical notes for patients (encrypted)
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notes')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Encrypted note content
    title = encrypt(models.CharField(max_length=200))
    content = encrypt(models.TextField())
    
    note_type = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Note'),
            ('diagnosis', 'Diagnosis'),
            ('treatment', 'Treatment Plan'),
            ('progress', 'Progress Note'),
            ('discharge', 'Discharge Summary'),
        ],
        default='general'
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.patient.patient_id} - {self.created_at}"
