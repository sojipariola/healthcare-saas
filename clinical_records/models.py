"""
Clinical records models with encrypted medical data
"""
from django.db import models
from django.contrib.auth.models import User
from healthcare_saas.fields import EncryptedTextField, EncryptedCharField
from patients.models import Patient
from appointments.models import Appointment


class ClinicalRecord(models.Model):
    """
    Main clinical record for patient encounters
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='clinical_records')
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clinical_record'
    )
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Encrypted clinical data
    chief_complaint = EncryptedTextField(help_text="Patient's main complaint")
    history_of_present_illness = EncryptedTextField(blank=True)
    
    # Vital signs
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    respiratory_rate = models.IntegerField(null=True, blank=True)
    oxygen_saturation = models.IntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Encrypted assessment and plan
    physical_examination = EncryptedTextField(blank=True)
    assessment = EncryptedTextField(blank=True)
    diagnosis = EncryptedTextField(blank=True)
    treatment_plan = EncryptedTextField(blank=True)
    
    # ICD-10 codes
    icd10_codes = models.JSONField(default=list, blank=True)
    
    # Timestamps
    encounter_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Immutability flag for audit compliance
    is_finalized = models.BooleanField(default=False)
    finalized_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-encounter_date']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['encounter_date']),
            models.Index(fields=['provider']),
        ]
    
    def __str__(self):
        return f"Clinical Record: {self.patient.patient_id} - {self.encounter_date}"


class Prescription(models.Model):
    """
    Prescription model with encrypted medication information
    """
    clinical_record = models.ForeignKey(
        ClinicalRecord,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    prescribed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Encrypted prescription details
    medication_name = EncryptedCharField(max_length=200)
    dosage = EncryptedCharField(max_length=100)
    frequency = EncryptedCharField(max_length=100)
    duration = EncryptedCharField(max_length=100)
    instructions = EncryptedTextField(blank=True)
    
    # Prescription metadata
    quantity = models.IntegerField()
    refills_allowed = models.IntegerField(default=0)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('expired', 'Expired'),
        ],
        default='active'
    )
    
    # Timestamps
    prescribed_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-prescribed_date']
    
    def __str__(self):
        return f"Prescription: {self.medication_name} for {self.patient.patient_id}"


class LabResult(models.Model):
    """
    Laboratory test results (encrypted)
    """
    clinical_record = models.ForeignKey(
        ClinicalRecord,
        on_delete=models.CASCADE,
        related_name='lab_results',
        null=True,
        blank=True
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    ordered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Test information
    test_name = models.CharField(max_length=200)
    test_code = models.CharField(max_length=50, blank=True)
    
    # Encrypted results
    result_value = EncryptedTextField()
    result_unit = models.CharField(max_length=50, blank=True)
    reference_range = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    
    is_abnormal = models.BooleanField(default=False)
    notes = EncryptedTextField(blank=True)
    
    # Timestamps
    ordered_date = models.DateTimeField(auto_now_add=True)
    result_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-ordered_date']
    
    def __str__(self):
        return f"Lab: {self.test_name} for {self.patient.patient_id}"


class ImagingStudy(models.Model):
    """
    Medical imaging studies (X-ray, MRI, CT, etc.)
    """
    clinical_record = models.ForeignKey(
        ClinicalRecord,
        on_delete=models.CASCADE,
        related_name='imaging_studies',
        null=True,
        blank=True
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='imaging_studies')
    ordered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    study_type = models.CharField(
        max_length=50,
        choices=[
            ('xray', 'X-Ray'),
            ('ct', 'CT Scan'),
            ('mri', 'MRI'),
            ('ultrasound', 'Ultrasound'),
            ('pet', 'PET Scan'),
            ('mammogram', 'Mammogram'),
        ]
    )
    
    body_part = models.CharField(max_length=100)
    
    # Encrypted findings
    findings = EncryptedTextField(blank=True)
    impression = EncryptedTextField(blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled'
    )
    
    # Image storage (encrypted path)
    image_url = EncryptedCharField(max_length=500, blank=True)
    
    # Timestamps
    ordered_date = models.DateTimeField(auto_now_add=True)
    study_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-ordered_date']
    
    def __str__(self):
        return f"{self.study_type} - {self.body_part} for {self.patient.patient_id}"
