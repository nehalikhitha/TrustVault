
from django.conf import settings
from django.db import models


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        DOCUMENT_SHARED = "DOCUMENT_SHARED", "Document Shared"
        PERMISSION_GRANTED = "PERMISSION_GRANTED", "Permission Granted"
        PERMISSION_REVOKED = "PERMISSION_REVOKED", "Permission Revoked"
        DOCUMENT_UPDATED = "DOCUMENT_UPDATED", "Document Updated"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_notifications"
    )

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices
    )

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient.username} - {self.notification_type}"