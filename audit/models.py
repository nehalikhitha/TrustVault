
from django.conf import settings
from django.db import models


class AuditEvent(models.Model):

    class EventType(models.TextChoices):
        LOGIN = "LOGIN", "Login"
        LOGOUT = "LOGOUT", "Logout"
        UPLOAD = "UPLOAD", "Document Upload"
        DOWNLOAD = "DOWNLOAD", "Document Download"
        VIEW = "VIEW", "Document View"
        EDIT = "EDIT", "Document Edit"
        DELETE = "DELETE", "Document Delete"
        PERMISSION_GRANTED = "PERMISSION_GRANTED", "Permission Granted"
        PERMISSION_REVOKED = "PERMISSION_REVOKED", "Permission Revoked"
        ACCESS_DENIED = "ACCESS_DENIED", "Access Denied"

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_events"
    )

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_events"
    )

    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_audit_events"
    )

    event_type = models.CharField(
        max_length=30,
        choices=EventType.choices,
        db_index=True
    )

    description = models.TextField(blank=True)

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(blank=True)

    details = models.JSONField(default=dict, blank=True)

    previous_hash = models.CharField(
        max_length=64,
        blank=True
    )

    event_hash = models.CharField(
        max_length=64,
        blank=True,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} - {self.created_at}"
