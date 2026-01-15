from django.test import TestCase
from django.urls import reverse
from .models import Document
from users.models import User

class DocumentUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_document_upload_view(self):
        response = self.client.get(reverse('document_upload'))
        self.assertEqual(response.status_code, 200)
        # You can add more tests for POST/upload logic if needed
