from django.urls import path, include, re_path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import home


def favicon(request):
    return HttpResponse(status=204)


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    re_path(r"^favicon.ico$", favicon),
    path(
        "api/v1/",
        include(
            [
                path("schema-viewer/", include("schema_viewer.urls")),
                path("auth/", include("apps.auths.urls")),
                path("companies/", include("apps.companies.urls")),
                path("attendance/", include("apps.attendance.urls")),
                path("reports/", include("apps.reports.urls")),
            ]
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
