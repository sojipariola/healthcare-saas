
from django.test import TestCase
from django.urls import reverse

from tenants.models import Tenant
from patients.models import Patient
from .models import ClinicalRecord



from users.models import CustomUser

class ClinicalRecordListViewTest(TestCase):
	def setUp(self):
		self.tenant = Tenant.objects.create(name="Test Tenant", subdomain="testtenant")
		self.user = CustomUser.objects.create_user(username="testuser", password="testpass", tenant=self.tenant)
		self.client.login(username="testuser", password="testpass")
		patient = Patient.objects.create(first_name="Alice", last_name="Brown", date_of_birth="1970-12-12", tenant=self.tenant)
		ClinicalRecord.objects.create(patient=patient, note="Initial note.", tenant=self.tenant)

	def test_clinicalrecord_list_view(self):
		response = self.client.get(reverse("clinicalrecord_list"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Alice Brown")
