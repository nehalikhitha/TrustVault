
from django.conf import settings
from django.db import models


class DocumentPermission(models.Model):

    class AccessLevel(models.TextChoices):
        READ = "READ", "Read"
        EDIT = "EDIT", "Edit"

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.CASCADE,
        related_name="permissions"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="document_permissions"
    )

    access_level = models.CharField(
        max_length=10,
        choices=AccessLevel.choices,
        default=AccessLevel.READ
    )

    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="granted_document_permissions"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["document", "user"],
                name="unique_document_user_permission"
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.document.title} - "
            f"{self.access_level}"
        )
