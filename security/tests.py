
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import PermissionDenied
from unittest.mock import patch

from documents.models import Document
from permissions.models import DocumentPermission
from security.services import require_document_access

User = get_user_model()


class DocumentAccessTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="Owner@123"
        )

        self.viewer = User.objects.create_user(
            username="viewer",
            password="Viewer@123"
        )

        self.editor = User.objects.create_user(
            username="editor",
            password="Editor@123"
        )

        self.document = Document.objects.create(
            title="Security Test Document",
            description="Testing document access",
            owner=self.owner,
            file=SimpleUploadedFile(
                "test.txt",
                b"TrustVault test content"
            )
        )

    def test_owner_has_read_access(self):
        self.assertTrue(
            require_document_access(
                self.document, self.owner, "READ"
            )
        )

    def test_owner_has_edit_access(self):
        self.assertTrue(
            require_document_access(
                self.document, self.owner, "EDIT"
            )
        )

    def test_viewer_with_read_permission(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            access_level="READ",
            granted_by=self.owner
        )

        self.assertTrue(
            require_document_access(
                self.document, self.viewer, "READ"
            )
        )

    def test_viewer_cannot_edit(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            access_level="READ",
            granted_by=self.owner
        )

        with patch("security.services.record_audit_event"):
            with self.assertRaises(PermissionError):
                require_document_access(
                    self.document, self.viewer, "EDIT"
                )

    def test_editor_has_edit_access(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.editor,
            access_level="EDIT",
            granted_by=self.owner
        )

        self.assertTrue(
            require_document_access(
                self.document, self.editor, "EDIT"
            )
        )

    def test_user_without_permission_is_denied(self):
        with patch("security.services.record_audit_event") as mock_audit:
            with self.assertRaises(PermissionError):
                require_document_access(
                    self.document, self.viewer, "READ"
                )

            mock_audit.assert_called_once()

    def test_invalid_access_level(self):
        with self.assertRaises(ValueError):
            require_document_access(
                self.document, self.viewer, "DELETE"
            )
