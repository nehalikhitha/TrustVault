
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from documents.models import Document
from documents.serializers import DocumentSerializer


class DocumentSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Only documents accessible to the logged-in user
        documents = Document.objects.filter(
            Q(owner=request.user)
            | Q(permissions__user=request.user)
        ).distinct()

        # Search by document title
        title = request.query_params.get("title")
        if title:
            documents = documents.filter(
                title__icontains=title
            )

        # Search by owner username
        owner = request.query_params.get("owner")
        if owner:
            documents = documents.filter(
                owner__username__icontains=owner
            )

        # Search by category
        category = request.query_params.get("category")
        if category:
            documents = documents.filter(
                category=category.upper()
            )

        # Search by starting date
        date_from = request.query_params.get("date_from")
        if date_from:
            documents = documents.filter(
                created_at__date__gte=date_from
            )

        # Search by ending date
        date_to = request.query_params.get("date_to")
        if date_to:
            documents = documents.filter(
                created_at__date__lte=date_to
            )

        serializer = DocumentSerializer(
            documents,
            many=True
        )

        data = serializer.data

        # Do not expose direct file URLs
        for item in data:
            item.pop("file", None)

        return Response({
            "count": len(data),
            "results": data
        })
