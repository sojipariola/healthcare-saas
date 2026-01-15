
from django.test import TestCase
from django.urls import reverse

from tenants.models import Tenant
from .models import Patient



from users.models import CustomUser

class PatientListViewTest(TestCase):
	def setUp(self):
		self.tenant = Tenant.objects.create(name="Test Tenant", subdomain="testtenant")
		self.user = CustomUser.objects.create_user(username="testuser", password="testpass", tenant=self.tenant)
		self.client.login(username="testuser", password="testpass")
		Patient.objects.create(first_name="John", last_name="Doe", date_of_birth="1990-01-01", tenant=self.tenant)

	def test_patient_list_view(self):
		response = self.client.get(reverse("patient_list"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "John Doe")
