
from .models import Notification


def create_notification(
    recipient,
    notification_type,
    message,
    actor=None,
    document=None,
):
    """
    Create a notification for a user.
    """

    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        document=document,
        notification_type=notification_type,
        message=message,
    )

    return notification
