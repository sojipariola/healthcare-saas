from django.test import TestCase
from .permissions import has_permission

class PermissionsTest(TestCase):
    def test_has_permission(self):
        self.assertIn(has_permission.__name__, dir(has_permission))
