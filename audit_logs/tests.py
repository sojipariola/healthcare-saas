from django.test import TestCase
from .models import AuditLog
from tenants.models import Tenant
from users.models import CustomUser

class AuditLogModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test Tenant", subdomain="testtenant")
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass", tenant=self.tenant)
        AuditLog.objects.create(action="login", user=self.user, tenant=self.tenant)

    def test_audit_log_created(self):
        log = AuditLog.objects.get(action="login")
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.tenant, self.tenant)
