
from django.db import models
from django.contrib.auth.models import AbstractUser
from tenants.models import Tenant

class CustomUser(AbstractUser):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users")
	role = models.CharField(max_length=50, default="user")

	def __str__(self):
		return f"{self.username} ({self.tenant})"
