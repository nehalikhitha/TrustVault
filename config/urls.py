
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Homepage and Dashboard
    path("", include("core.urls")),

    # Authentication
    path("accounts/", include("accounts.urls")),

    # Application APIs
    path("api/documents/", include("documents.urls")),
    path("api/permissions/", include("permissions.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/search/", include("search.urls")),
    path("api/audit/", include("audit.urls")),
]
