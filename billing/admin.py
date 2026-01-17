"""
Admin configuration for Billing
"""
from django.contrib import admin
from .models import Invoice, InvoiceLineItem, Payment, InsuranceClaim


class InvoiceLineItemInline(admin.TabularInline):
    model = InvoiceLineItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'patient', 'issue_date', 'due_date', 'total_amount', 'status']
    list_filter = ['status', 'issue_date']
    search_fields = ['invoice_number', 'patient__patient_id']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [InvoiceLineItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'amount', 'payment_method', 'payment_date', 'processed_by']
    list_filter = ['payment_date', 'payment_method']
    search_fields = ['invoice__invoice_number', 'transaction_id']
    readonly_fields = ['payment_date']


@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ['claim_number', 'patient', 'claim_amount', 'approved_amount', 'status']
    list_filter = ['status', 'submitted_date']
    search_fields = ['claim_number', 'patient__patient_id']
    readonly_fields = ['created_at', 'updated_at']
