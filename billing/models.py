from django.db import models
from tenants.models import Tenant
from patients.models import Patient

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    interval = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TenantSubscription(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    last_payment = models.DateTimeField(null=True, blank=True)
    next_payment_due = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.tenant} - {self.plan}"

class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    is_subscription = models.BooleanField(default=False)
    external_id = models.CharField(max_length=100, blank=True)  # For gateway reference

    def __str__(self):
        return f"{self.tenant} - {self.amount} {self.currency} ({'Subscription' if self.is_subscription else 'One-time'})"
