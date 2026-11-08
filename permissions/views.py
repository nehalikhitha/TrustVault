
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from documents.models import Document
from .models import DocumentPermission
from .serializers import DocumentPermissionSerializer
from .services import (
    grant_document_access,
    revoke_document_access,
)

User = get_user_model()


class DocumentPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, document_id):
        document = get_object_or_404(
            Document,
            id=document_id
        )

        user_id = request.data.get("user_id")
        access_level = request.data.get("access_level")

        if not user_id or not access_level:
            return Response(
                {"error": "user_id and access_level are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=user_id)

        try:
            permission = grant_document_access(
                document=document,
                user=user,
                access_level=access_level,
                actor=request.user,
            )
        except PermissionError as exc:
            raise PermissionDenied(str(exc))
        except ValueError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DocumentPermissionSerializer(permission)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, document_id, user_id):
        document = get_object_or_404(
            Document,
            id=document_id
        )

        user = get_object_or_404(User, id=user_id)

        try:
            revoked = revoke_document_access(
                document=document,
                user=user,
                actor=request.user,
            )
        except PermissionError as exc:
            raise PermissionDenied(str(exc))

        if not revoked:
            return Response(
                {"message": "Permission not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"message": "Permission revoked successfully."},
            status=status.HTTP_200_OK
        )
