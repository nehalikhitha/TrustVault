from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import AuditEvent
from .serializers import AuditEventSerializer


class AuditLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "ADMIN":
            raise PermissionDenied(
                "Only admins can view audit logs."
            )

        events = AuditEvent.objects.select_related(
            "actor",
            "document",
            "target_user",
        ).all()

        event_type = request.query_params.get("event_type")

        if event_type:
            events = events.filter(event_type=event_type.upper())

        serializer = AuditEventSerializer(events, many=True)

        return Response({
            "count": events.count(),
            "results": serializer.data,
        })