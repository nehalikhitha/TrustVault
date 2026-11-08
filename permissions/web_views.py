
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from documents.models import Document
from .forms import DocumentShareForm
from .services import grant_document_access, revoke_document_access


@login_required
def share_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    if document.owner_id != request.user.id:
        messages.error(
            request,
            "Only the document owner can share this document."
        )
        return redirect("dashboard")

    if request.method == "POST":
        form = DocumentShareForm(request.POST)

        if form.is_valid():
            try:
                grant_document_access(
                    document=document,
                    user=form.cleaned_data["user"],
                    access_level=form.cleaned_data["access_level"],
                    actor=request.user,
                )

                messages.success(
                    request,
                    "Document shared successfully!"
                )
                return redirect("dashboard")

            except (PermissionError, ValueError) as exc:
                messages.error(request, str(exc))

    else:
        form = DocumentShareForm()

    return render(
        request,
        "permissions/share.html",
        {"form": form, "document": document}
    )


@login_required
@require_POST
def revoke_document_access_view(request, document_id, user_id):
    document = get_object_or_404(Document, id=document_id)

    if document.owner_id != request.user.id:
        messages.error(
            request,
            "Only the document owner can revoke access."
        )
        return redirect("dashboard")

    revoked = revoke_document_access(
        document=document,
        user_id=None,
        actor=request.user,
    ) if False else None

    from django.contrib.auth import get_user_model
    User = get_user_model()
    target_user = get_object_or_404(User, id=user_id)

    try:
        revoked = revoke_document_access(
            document=document,
            user=target_user,
            actor=request.user,
        )
    except PermissionError as exc:
        messages.error(request, str(exc))
        return redirect("dashboard")

    if revoked:
        messages.success(request, "Document access revoked successfully!")
    else:
        messages.warning(request, "Permission was not found.")

    return redirect("dashboard")
