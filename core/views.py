
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch

from documents.models import Document
from permissions.models import DocumentPermission


def home(request):
    return render(request, "core/home.html")


@login_required
def dashboard(request):
    documents = (
        Document.objects.filter(
            Q(owner=request.user) |
            Q(permissions__user=request.user)
        )
        .distinct()
        .prefetch_related(
            Prefetch(
                "permissions",
                queryset=DocumentPermission.objects.select_related("user")
            )
        )
    )

    return render(
        request,
        "core/dashboard.html",
        {"documents": documents}
    )
