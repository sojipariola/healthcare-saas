from datetime import timedelta
from django.utils import timezone
from tenants.models import Tenant
from users.models import CustomUser
from patients.models import Patient
from django.core.mail import send_mail
from django.conf import settings

FREE_TRIAL_DAYS = 90
MAX_FREE_USERS = 2
MAX_FREE_PATIENTS = 5


def is_tenant_in_free_trial(tenant):
    return (timezone.now() - tenant.created_at).days < FREE_TRIAL_DAYS

def free_trial_days_left(tenant):
    days_used = (timezone.now() - tenant.created_at).days
    return max(0, FREE_TRIAL_DAYS - days_used)

def is_free_user_limit_reached(tenant):
    return CustomUser.objects.filter(tenant=tenant).count() >= MAX_FREE_USERS

def is_free_patient_limit_reached(tenant):
    return Patient.objects.filter(tenant=tenant).count() >= MAX_FREE_PATIENTS

def send_trial_expiry_notification(tenant):
    admin_users = CustomUser.objects.filter(tenant=tenant, role__in=["admin", "owner"])
    days_left = free_trial_days_left(tenant)
    subject = f"ClinicCloud Free Trial Expiry Warning"
    message = (
        f"Your free trial for tenant '{tenant.name}' will expire in {days_left} days. "
        f"Upgrade soon to avoid loss of data and service interruption. "
        f"Limits: max {MAX_FREE_USERS} users, {MAX_FREE_PATIENTS} patients."
    )
    for admin in admin_users:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin.email])
