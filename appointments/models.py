"""
Appointment scheduling models
"""
from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient


class Appointment(models.Model):
    """
    Appointment scheduling model
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='appointments')
    
    # Appointment details
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration_minutes = models.IntegerField(default=30)
    
    appointment_type = models.CharField(
        max_length=50,
        choices=[
            ('checkup', 'Regular Checkup'),
            ('consultation', 'Consultation'),
            ('followup', 'Follow-up'),
            ('emergency', 'Emergency'),
            ('vaccination', 'Vaccination'),
            ('lab_work', 'Lab Work'),
            ('imaging', 'Imaging'),
            ('therapy', 'Therapy'),
        ],
        default='consultation'
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('confirmed', 'Confirmed'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show'),
        ],
        default='scheduled'
    )
    
    # Additional information
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Reminder settings
    reminder_sent = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancelled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cancelled_appointments'
    )
    
    class Meta:
        ordering = ['appointment_date', 'appointment_time']
        indexes = [
            models.Index(fields=['appointment_date', 'appointment_time']),
            models.Index(fields=['status']),
            models.Index(fields=['patient']),
            models.Index(fields=['provider']),
        ]
    
    def __str__(self):
        return f"Appointment: {self.patient.patient_id} - {self.appointment_date} {self.appointment_time}"


class AppointmentSlot(models.Model):
    """
    Available time slots for appointments
    """
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='available_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['provider', 'date', 'start_time']
    
    def __str__(self):
        return f"{self.provider.username} - {self.date} {self.start_time}-{self.end_time}"
