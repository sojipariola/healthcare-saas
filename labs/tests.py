
from django.test import TestCase
from django.urls import reverse

from tenants.models import Tenant
from patients.models import Patient
from .models import LabResult



from users.models import CustomUser

class LabResultListViewTest(TestCase):
	def setUp(self):
		self.tenant = Tenant.objects.create(name="Test Tenant", subdomain="testtenant")
		self.user = CustomUser.objects.create_user(username="testuser", password="testpass", tenant=self.tenant)
		self.client.login(username="testuser", password="testpass")
		patient = Patient.objects.create(first_name="Bob", last_name="White", date_of_birth="2000-06-06", tenant=self.tenant)
		LabResult.objects.create(patient=patient, result="Normal.", tenant=self.tenant)

	def test_labresult_list_view(self):
		response = self.client.get(reverse("labresult_list"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Bob White")
