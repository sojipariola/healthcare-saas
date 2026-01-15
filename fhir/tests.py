from datetime import date
from django.test import TestCase
from django.urls import reverse
from patients.models import Patient
from tenants.models import Tenant

class FhirPatientTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test Clinic", subdomain="test")
        self.patient = Patient.objects.create(
            tenant=self.tenant,
            first_name="Ada",
            last_name="Lovelace",
            date_of_birth=date(1815, 12, 10),
            email="ada@example.com",
            phone="555-1234",
        )

    def test_patient_read_returns_fhir_patient(self):
        url = reverse("fhir_patient_read", args=[self.patient.pk])
        resp = self.client.get(f"{url}?tenant_id={self.tenant.id}")
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["resourceType"], "Patient")
        self.assertEqual(body["id"], str(self.patient.id))
        self.assertEqual(body["identifier"][0]["value"], str(self.tenant.id))
        self.assertEqual(body["name"][0]["family"], "Lovelace")
        self.assertEqual(body["telecom"][0]["system"], "phone")

    def test_patient_read_requires_tenant(self):
        url = reverse("fhir_patient_read", args=[self.patient.pk])
        resp = self.client.get(url)  # missing tenant_id
        self.assertEqual(resp.status_code, 400)
