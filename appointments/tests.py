
from django.test import TestCase
from django.urls import reverse

from tenants.models import Tenant
from patients.models import Patient
from .models import Appointment
from datetime import datetime



from users.models import CustomUser

class AppointmentListViewTest(TestCase):
	def setUp(self):
		self.tenant = Tenant.objects.create(name="Test Tenant", subdomain="testtenant")
		self.user = CustomUser.objects.create_user(username="testuser", password="testpass", tenant=self.tenant)
		self.client.login(username="testuser", password="testpass")
		patient = Patient.objects.create(first_name="Jane", last_name="Smith", date_of_birth="1985-05-05", tenant=self.tenant)
		Appointment.objects.create(patient=patient, scheduled_for="2026-01-10T10:00:00Z", status="scheduled", tenant=self.tenant)

	def test_appointment_list_view(self):
		response = self.client.get(reverse("appointment_list"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Jane Smith")
