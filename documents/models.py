
from django.conf import settings
from django.db import models


class Document(models.Model):

    class Category(models.TextChoices):
        GENERAL = "GENERAL", "General"
        BUSINESS = "BUSINESS", "Business"
        FINANCIAL = "FINANCIAL", "Financial"
        LEGAL = "LEGAL", "Legal"
        PERSONAL = "PERSONAL", "Personal"
        OTHER = "OTHER", "Other"

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.GENERAL
    )

    file = models.FileField(upload_to="documents/")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_documents"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
