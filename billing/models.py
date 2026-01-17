"""
Billing and invoicing models
"""
from django.db import models
from django.contrib.auth.models import User
from healthcare_saas.fields import EncryptedCharField, EncryptedTextField
from patients.models import Patient
from appointments.models import Appointment
from clinical_records.models import ClinicalRecord


class Invoice(models.Model):
    """
    Invoice model for billing
    """
    invoice_number = models.CharField(max_length=50, unique=True, db_index=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices'
    )
    clinical_record = models.ForeignKey(
        ClinicalRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices'
    )
    
    # Invoice details
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('issued', 'Issued'),
            ('paid', 'Paid'),
            ('partial', 'Partially Paid'),
            ('overdue', 'Overdue'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft'
    )
    
    # Payment information (encrypted)
    payment_method = EncryptedCharField(
        max_length=50,
        choices=[
            ('cash', 'Cash'),
            ('credit_card', 'Credit Card'),
            ('debit_card', 'Debit Card'),
            ('insurance', 'Insurance'),
            ('bank_transfer', 'Bank Transfer'),
            ('check', 'Check'),
        ],
        blank=True
    )
    
    payment_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Insurance claim information
    insurance_claim_number = EncryptedCharField(max_length=100, blank=True)
    insurance_paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    patient_responsibility = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issue_date']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['patient']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.patient.patient_id}"
    
    def calculate_total(self):
        """Calculate total from line items"""
        self.subtotal = sum(item.total for item in self.line_items.all())
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        self.save()


class InvoiceLineItem(models.Model):
    """
    Individual line items on an invoice
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='line_items')
    
    description = models.CharField(max_length=255)
    
    # CPT/HCPCS codes for medical procedures
    procedure_code = models.CharField(max_length=20, blank=True)
    
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.description} - ${self.total}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate total"""
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Payment(models.Model):
    """
    Payment records
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    payment_method = EncryptedCharField(
        max_length=50,
        choices=[
            ('cash', 'Cash'),
            ('credit_card', 'Credit Card'),
            ('debit_card', 'Debit Card'),
            ('insurance', 'Insurance'),
            ('bank_transfer', 'Bank Transfer'),
            ('check', 'Check'),
        ]
    )
    
    # Encrypted transaction details
    transaction_id = EncryptedCharField(max_length=100, blank=True)
    reference_number = EncryptedCharField(max_length=100, blank=True)
    
    notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment ${self.amount} for Invoice {self.invoice.invoice_number}"


class InsuranceClaim(models.Model):
    """
    Insurance claim tracking
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='insurance_claims')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='insurance_claims')
    
    # Claim information (encrypted)
    claim_number = EncryptedCharField(max_length=100, unique=True)
    insurance_provider = EncryptedCharField(max_length=200)
    policy_number = EncryptedCharField(max_length=100)
    
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('submitted', 'Submitted'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('partially_approved', 'Partially Approved'),
            ('denied', 'Denied'),
            ('appealed', 'Appealed'),
        ],
        default='pending'
    )
    
    # Timestamps
    submitted_date = models.DateTimeField(null=True, blank=True)
    response_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    notes = EncryptedTextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Claim {self.claim_number} - {self.status}"
