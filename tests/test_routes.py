from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tenants.models import Tenant

class RouteSmokeTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test Clinic", subdomain="test")
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123", tenant=self.tenant, is_active=True
        )
        self.client.login(username="testuser", password="testpass123", tenant=self.tenant)

    def test_landing_page(self):
        resp = self.client.get(reverse("landing"))
        self.assertEqual(resp.status_code, 200)

    def test_patients_routes(self):
        for name in ["patient_list", "patient_create"]:
            resp = self.client.get(reverse(name))
            self.assertIn(resp.status_code, [200, 302])

    def test_appointments_routes(self):
        for name in ["appointment_list", "appointment_create"]:
            resp = self.client.get(reverse(name))
            self.assertIn(resp.status_code, [200, 302])

    def test_clinical_records_routes(self):
        for name in ["clinicalrecord_list", "clinicalrecord_create"]:
            resp = self.client.get(reverse(name))
            self.assertIn(resp.status_code, [200, 302])

    def test_labs_routes(self):
        for name in ["labresult_list", "labresult_create"]:
            resp = self.client.get(reverse(name))
            self.assertIn(resp.status_code, [200, 302])

    def test_login_logout(self):
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)
        # Django's LogoutView expects POST by default for security
        resp = self.client.post(reverse("logout"))
        self.assertIn(resp.status_code, [200, 302])

    def test_register(self):
        resp = self.client.get(reverse("register"))
        self.assertEqual(resp.status_code, 200)

    def test_password_reset(self):
        resp = self.client.get(reverse("password_reset"))
        self.assertEqual(resp.status_code, 200)
