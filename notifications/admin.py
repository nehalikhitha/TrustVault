from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "recipient",
        "actor",
        "document",
        "notification_type",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "recipient__username",
        "actor__username",
        "document__title",
        "message",
    )

    readonly_fields = (
        "recipient",
        "actor",
        "document",
        "notification_type",
        "message",
        "created_at",
    )

    ordering = ("-created_at",)
