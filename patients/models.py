

from django.db import models
from tenants.models import Tenant

class Patient(models.Model):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="patients")
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField()
	email = models.EmailField(blank=True, null=True)
	phone = models.CharField(max_length=20, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"
