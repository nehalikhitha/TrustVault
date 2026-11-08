
import hashlib
import json

from django.db import transaction

from .models import AuditEvent


@transaction.atomic
def record_audit_event(
    event_type,
    actor=None,
    document=None,
    target_user=None,
    description="",
    ip_address=None,
    user_agent="",
    details=None,
):
    details = details or {}

    latest_event = (
        AuditEvent.objects
        .select_for_update()
        .order_by("-id")
        .first()
    )

    previous_hash = (
        latest_event.event_hash
        if latest_event and latest_event.event_hash
        else ""
    )

    audit_data = {
        "actor_id": actor.id if actor else None,
        "document_id": document.id if document else None,
        "target_user_id": target_user.id if target_user else None,
        "event_type": event_type,
        "description": description,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "details": details,
        "previous_hash": previous_hash,
    }

    serialized_data = json.dumps(
        audit_data,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )

    event_hash = hashlib.sha256(
        serialized_data.encode("utf-8")
    ).hexdigest()

    return AuditEvent.objects.create(
        actor=actor,
        document=document,
        target_user=target_user,
        event_type=event_type,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
        previous_hash=previous_hash,
        event_hash=event_hash,
    )
