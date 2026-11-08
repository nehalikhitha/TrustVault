from django.test import TestCase
from django.contrib.auth import get_user_model
from notifications.models import Notification

User = get_user_model()


class NotificationTests(TestCase):

    def setUp(self):
        self.recipient = User.objects.create_user(
            username="recipient",
            password="Test@123"
        )

        self.actor = User.objects.create_user(
            username="actor",
            password="Test@123"
        )

    def test_notification_creation(self):
        notification = Notification.objects.create(
            recipient=self.recipient,
            actor=self.actor,
            notification_type=Notification.NotificationType.DOCUMENT_SHARED,
            message="A document was shared with you"
        )

        self.assertEqual(notification.recipient, self.recipient)
        self.assertEqual(notification.actor, self.actor)

    def test_notification_default_unread(self):
        notification = Notification.objects.create(
            recipient=self.recipient,
            notification_type=Notification.NotificationType.PERMISSION_GRANTED,
            message="Permission granted"
        )

        self.assertFalse(notification.is_read)

    def test_notification_can_be_marked_read(self):
        notification = Notification.objects.create(
            recipient=self.recipient,
            notification_type=Notification.NotificationType.DOCUMENT_UPDATED,
            message="Document updated"
        )

        notification.is_read = True
        notification.save()

        notification.refresh_from_db()
        self.assertTrue(notification.is_read)