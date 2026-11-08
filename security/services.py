
from permissions.models import DocumentPermission
from audit.models import AuditEvent
from audit.services import record_audit_event


def require_document_access(
    document,
    user,
    required_access="READ",
    ip_address=None,
    user_agent="",
):
    """
    Verify whether a user can access a document.

    READ: View or download.
    EDIT: Modify the document.
    """

    if required_access not in ["READ", "EDIT"]:
        raise ValueError("Invalid access level.")

    # Document owner always has access
    if document.owner_id == user.id:
        return True

    # Check current database permission
    permission = DocumentPermission.objects.filter(
        document=document,
        user=user,
    ).first()

    allowed = False

    if permission:
        if permission.access_level == "EDIT":
            allowed = True
        elif (
            permission.access_level == "READ"
            and required_access == "READ"
        ):
            allowed = True

    if allowed:
        return True

    # Record unauthorized access attempt
    record_audit_event(
        event_type=AuditEvent.EventType.ACCESS_DENIED,
        actor=user,
        document=document,
        description=(
            f"Unauthorized {required_access} access attempt."
        ),
        ip_address=ip_address,
        user_agent=user_agent,
        details={
            "required_access": required_access,
        },
    )

    raise PermissionError(
        "You do not have permission to access this document."
    )
