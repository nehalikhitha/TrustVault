from django.test import TestCase
from django.contrib.auth import get_user_model
from audit.models import AuditEvent

User = get_user_model()


class AuditEventTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="audituser",
            password="Audit@123"
        )

    def test_audit_event_creation(self):
        event = AuditEvent.objects.create(
            actor=self.user,
            event_type="LOGIN"
        )

        self.assertEqual(event.actor, self.user)
        self.assertEqual(event.event_type, "LOGIN")

    def test_audit_event_has_timestamp(self):
        event = AuditEvent.objects.create(
            actor=self.user,
            event_type="LOGIN"
        )

        self.assertIsNotNone(event.created_at)