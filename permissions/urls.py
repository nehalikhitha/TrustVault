
from django.urls import path

from .views import DocumentPermissionView


urlpatterns = [
    path(
        "documents/<int:document_id>/permissions/",
        DocumentPermissionView.as_view(),
        name="document-permissions",
    ),
    path(
        "documents/<int:document_id>/permissions/<int:user_id>/",
        DocumentPermissionView.as_view(),
        name="revoke-document-permission",
    ),
]
