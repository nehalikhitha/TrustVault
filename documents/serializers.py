
from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    owner_username = serializers.CharField(
        source="owner.username",
        read_only=True
    )

    class Meta:
        model = Document

        fields = [
            "id",
            "title",
            "description",
            "category",
            "file",
            "owner",
            "owner_username",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "owner_username",
            "created_at",
            "updated_at",
        ]
