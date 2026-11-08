
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Document
from .serializers import DocumentSerializer

from audit.models import AuditEvent
from audit.services import record_audit_event
from security.services import require_document_access


def get_client_ip(request):
    return request.META.get("REMOTE_ADDR")


def get_user_agent(request):
    return request.META.get("HTTP_USER_AGENT", "")


def check_access(document, request, access_level="READ"):
    try:
        return require_document_access(
            document=document,
            user=request.user,
            required_access=access_level,
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
        )
    except PermissionError as exc:
        raise PermissionDenied(str(exc))


class DocumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        documents = Document.objects.filter(
            Q(owner=request.user)
            | Q(permissions__user=request.user)
        ).distinct()

        serializer = DocumentSerializer(documents, many=True)
        data = serializer.data

        for item in data:
            item.pop("file", None)

        return Response(data)

    def post(self, request):

        # Only OWNER can upload documents
        if request.user.role != "OWNER":

            record_audit_event(
                event_type=AuditEvent.EventType.ACCESS_DENIED,
                actor=request.user,
                description="Unauthorized document upload attempt.",
                ip_address=get_client_ip(request),
                user_agent=get_user_agent(request),
            )

            raise PermissionDenied(
                "Only document owners can upload documents."
            )

        serializer = DocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document = serializer.save(owner=request.user)

        record_audit_event(
            event_type=AuditEvent.EventType.UPLOAD,
            actor=request.user,
            document=document,
            description="Document uploaded successfully.",
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
        )

        data = DocumentSerializer(document).data
        data.pop("file", None)

        return Response(
            data,
            status=status.HTTP_201_CREATED
        )


class DocumentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_document(self, pk):
        return get_object_or_404(Document, pk=pk)

    def get(self, request, pk):
        document = self.get_document(pk)

        check_access(document, request, "READ")

        record_audit_event(
            event_type=AuditEvent.EventType.VIEW,
            actor=request.user,
            document=document,
            description="Document viewed.",
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
        )

        data = DocumentSerializer(document).data
        data.pop("file", None)

        return Response(data)

    def patch(self, request, pk):
        document = self.get_document(pk)

        check_access(document, request, "EDIT")

        serializer = DocumentSerializer(
            document,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        document = serializer.save()

        record_audit_event(
            event_type=AuditEvent.EventType.EDIT,
            actor=request.user,
            document=document,
            description="Document updated.",
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
        )

        data = DocumentSerializer(document).data
        data.pop("file", None)

        return Response(data)

    def delete(self, request, pk):
        document = self.get_document(pk)

        if document.owner_id != request.user.id:
            check_access(document, request, "EDIT")
            raise PermissionDenied(
                "Only the document owner can delete this document."
            )

        record_audit_event(
            event_type=AuditEvent.EventType.DELETE,
            actor=request.user,
            document=document,
            description="Document deleted.",
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
        )

        document.delete()

        return Response(
            {"message": "Document deleted successfully."},
            status=status.HTTP_200_OK
        )


class DocumentDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        document = get_object_or_404(Document, pk=pk)

        check_access(document, request, "READ")

        if not document.file:
            return Response(
                {"error": "Document file not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        record_audit_event(
            event_type=AuditEvent.EventType.DOWNLOAD,
            actor=request.user,
            document=document,
            description="Document downloaded.",
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
        )

        return FileResponse(
            document.file.open("rb"),
            as_attachment=True,
            filename=document.file.name.split("/")[-1]
        )
