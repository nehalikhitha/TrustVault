from django.test import TestCase
from django.contrib.auth import get_user_model
from documents.models import Document

User = get_user_model()


class DocumentModelTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="docowner",
            password="Owner@123"
        )

    def test_document_creation(self):
        document = Document.objects.create(
            title="Test Document",
            description="Testing TrustVault document",
            owner=self.owner
        )

        self.assertEqual(document.title, "Test Document")
        self.assertEqual(document.owner, self.owner)

    def test_document_has_owner(self):
        document = Document.objects.create(
            title="Owner Test",
            owner=self.owner
        )

        self.assertIsNotNone(document.owner)