
from rest_framework import serializers
from .models import AuditEvent


class AuditEventSerializer(serializers.ModelSerializer):

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

    target_username = serializers.CharField(
        source="target_user.username",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = AuditEvent

        fields = [
            "id",
            "actor",
            "actor_username",
            "document",
            "document_title",
            "target_user",
            "target_username",
            "event_type",
            "description",
            "ip_address",
            "user_agent",
            "details",
            "previous_hash",
            "event_hash",
            "created_at",
        ]

        read_only_fields = fields
