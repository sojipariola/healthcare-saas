from django.db import models
from users.models import CustomUser
from tenants.models import Tenant

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("user_approved", "User Approved"),
        ("user_registered", "User Registered"),
        ("login_failed", "Login Failed"),
        ("login_success", "Login Success"),
        # Add more as needed
    ]
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    tenant = models.ForeignKey(Tenant, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.action} by {self.user} ({self.tenant})"
