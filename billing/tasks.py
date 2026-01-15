from celery import shared_task
from tenants.models import Tenant
from billing.free_trial import is_tenant_in_free_trial, send_trial_expiry_notification, free_trial_days_left
from django.utils import timezone

@shared_task
def weekly_trial_expiry_notifications():
    for tenant in Tenant.objects.all():
        if is_tenant_in_free_trial(tenant):
            days_left = free_trial_days_left(tenant)
            if days_left <= 21:  # Notify in last 3 weeks
                send_trial_expiry_notification(tenant)
