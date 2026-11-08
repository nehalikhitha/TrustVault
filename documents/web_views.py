
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import DocumentUploadForm
from audit.models import AuditEvent
from audit.services import record_audit_event


@login_required
def upload_document(request):

    # Only OWNER users can upload documents
    if request.user.role != "OWNER":
        messages.error(
            request,
            "Only document owners can upload documents."
        )
        return redirect("dashboard")

    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()

            record_audit_event(
                event_type=AuditEvent.EventType.UPLOAD,
                actor=request.user,
                document=document,
                description="Document uploaded successfully.",
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )

            messages.success(
                request,
                "Document uploaded successfully!"
            )

            return redirect("dashboard")

    else:
        form = DocumentUploadForm()

    return render(
        request,
        "documents/upload.html",
        {"form": form}
    )
