
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    recipient_username = serializers.CharField(
        source="recipient.username",
        read_only=True
    )

    actor_username = serializers.CharField(
        source="actor.username",
        read_only=True,
        allow_null=True
    )

    document_title = serializers.CharField(
        source="document.title",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Notification

        fields = [
            "id",
            "recipient",
            "recipient_username",
            "actor",
            "actor_username",
            "document",
            "document_title",
            "notification_type",
            "message",
            "is_read",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "recipient",
            "recipient_username",
            "actor",
            "actor_username",
            "document",
            "document_title",
            "notification_type",
            "message",
            "created_at",
        ]
