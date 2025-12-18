from django.urls import path
from .views import (
    CompanyAttendancePDFView,
    EmployeeAttendancePDFView,
    MyAttendancePDFView,
)

urlpatterns = [
    path("pdf/company/", CompanyAttendancePDFView.as_view()),
    path("pdf/employee/<uuid:employee_id>/", EmployeeAttendancePDFView.as_view()),
    path("pdf/my/", MyAttendancePDFView.as_view()),
]
