from django.contrib import admin
from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "event_type",
        "actor",
        "document",
        "target_user",
        "ip_address",
        "created_at",
    )

    list_filter = (
        "event_type",
        "created_at",
    )

    search_fields = (
        "actor__username",
        "document__title",
        "target_user__username",
        "description",
    )

    readonly_fields = (
        "actor",
        "document",
        "target_user",
        "event_type",
        "description",
        "ip_address",
        "user_agent",
        "details",
        "previous_hash",
        "event_hash",
        "created_at",
    )

    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
