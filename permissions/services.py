
from django.db import transaction

from .models import DocumentPermission
from audit.models import AuditEvent
from audit.services import record_audit_event
from notifications.services import create_notification


@transaction.atomic
def grant_document_access(
    document,
    user,
    access_level,
    actor,
):
    # Only the document owner can share it
    if document.owner_id != actor.id:
        raise PermissionError(
            "Only the document owner can grant access."
        )

    if user.id == document.owner_id:
        raise ValueError(
            "The document owner already has full access."
        )

    if access_level not in DocumentPermission.AccessLevel.values:
        raise ValueError("Invalid access level.")

    permission, created = (
        DocumentPermission.objects.update_or_create(
            document=document,
            user=user,
            defaults={
                "access_level": access_level,
                "granted_by": actor,
            },
        )
    )

    event_type = (
        AuditEvent.EventType.PERMISSION_GRANTED
        if created
        else AuditEvent.EventType.PERMISSION_GRANTED
    )

    record_audit_event(
        event_type=event_type,
        actor=actor,
        document=document,
        target_user=user,
        description=f"{access_level} access granted or updated.",
        details={"access_level": access_level},
    )

    create_notification(
        recipient=user,
        actor=actor,
        document=document,
        notification_type=(
            "PERMISSION_GRANTED"
        ),
        message=(
            f"You have been granted {access_level} "
            f"access to {document.title}."
        ),
    )

    return permission


@transaction.atomic
def revoke_document_access(document, user, actor):
    # Only the document owner can revoke access
    if document.owner_id != actor.id:
        raise PermissionError(
            "Only the document owner can revoke access."
        )

    permission = DocumentPermission.objects.filter(
        document=document,
        user=user,
    ).first()

    if permission is None:
        return False

    permission.delete()

    record_audit_event(
        event_type=AuditEvent.EventType.PERMISSION_REVOKED,
        actor=actor,
        document=document,
        target_user=user,
        description="Document access revoked.",
    )

    create_notification(
        recipient=user,
        actor=actor,
        document=document,
        notification_type="PERMISSION_REVOKED",
        message=(
            f"Your access to {document.title} has been revoked."
        ),
    )

    return True
