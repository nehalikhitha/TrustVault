from django.contrib import admin
from .models import DocumentPermission


@admin.register(DocumentPermission)
class DocumentPermissionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "document",
        "user",
        "access_level",
        "granted_by",
        "created_at",
    )

    list_filter = (
        "access_level",
        "created_at",
    )

    search_fields = (
        "document__title",
        "user__username",
        "granted_by__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
