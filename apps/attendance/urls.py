from django.urls import path
from .views import (
    AdminAttendanceDetailAPIView,
    AdminAttendanceListAPIView,
    AttendanceCreateAPIView,
    EmployeeAttendanceListAPIView,
    UserDetailsRetrieveAPIView,
    UsersListAPIView,
)

urlpatterns = [
    path("my/", EmployeeAttendanceListAPIView.as_view(), name="employee-attendance-list"),
    path("admin/", AdminAttendanceListAPIView.as_view(), name="admin-attendance-list"),
    path("create/", AttendanceCreateAPIView.as_view(), name="attendance-create"),
    path(
        "employee/<str:uid>/info/",
        UserDetailsRetrieveAPIView.as_view(),
        name="employee-details",
    ),
    path("employees/", UsersListAPIView.as_view(), name="employee-list"),
    path(
        "<str:uid>/",
        AdminAttendanceDetailAPIView.as_view(),
        name="admin-attendance-detail",
    ),
]
