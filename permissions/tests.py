from django.test import TestCase
from django.contrib.auth import get_user_model
from documents.models import Document
from permissions.models import DocumentPermission

User = get_user_model()


class DocumentPermissionTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="Owner@123"
        )

        self.viewer = User.objects.create_user(
            username="viewer",
            password="Viewer@123"
        )

    def test_user_creation(self):
        self.assertNotEqual(self.owner, self.viewer)

    def test_owner_role_exists(self):
        self.assertIsNotNone(self.owner.role)

    def test_viewer_role_exists(self):
        self.assertIsNotNone(self.viewer.role)