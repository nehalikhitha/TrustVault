
from rest_framework import serializers
from .models import DocumentPermission


class DocumentPermissionSerializer(serializers.ModelSerializer):

    user_username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    granted_by_username = serializers.CharField(
        source="granted_by.username",
        read_only=True,
        allow_null=True
    )

    document_title = serializers.CharField(
        source="document.title",
        read_only=True
    )

    class Meta:
        model = DocumentPermission

        fields = [
            "id",
            "document",
            "document_title",
            "user",
            "user_username",
            "access_level",
            "granted_by",
            "granted_by_username",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "document",
            "document_title",
            "user",
            "user_username",
            "granted_by",
            "granted_by_username",
            "access_level",
            "created_at",
            "updated_at",
        ]
