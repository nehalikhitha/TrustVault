
from django.urls import path

from .views import home, dashboard
from permissions.web_views import (
    share_document,
    revoke_document_access_view,
)

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),

    path(
        "share-document/<int:document_id>/",
        share_document,
        name="share-document",
    ),

    path(
        "revoke-access/<int:document_id>/<int:user_id>/",
        revoke_document_access_view,
        name="revoke-document-access",
    ),
]
