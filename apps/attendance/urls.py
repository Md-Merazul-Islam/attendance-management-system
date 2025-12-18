from django.urls import path
from .views import (
    AdminAttendanceDetailAPIView,
    AdminAttendanceListAPIView,
    AttendanceCreateAPIView,
    EmployeeAttendanceListAPIView,
    UserDetailsRetrieveAPIView,
    AllUsersListAPIView,
    EmployeeAttendanceDetailAPIView
)

urlpatterns = [
    path("my-attendance/", EmployeeAttendanceListAPIView.as_view(), name="employee-attendance-list"),
    path("my-attendance/<str:uid>/", EmployeeAttendanceDetailAPIView.as_view(), name="employee-attendance-detail"),
    path("admin/", AdminAttendanceListAPIView.as_view(), name="admin-attendance-list"),
    path("create/", AttendanceCreateAPIView.as_view(), name="attendance-create"),
    path( "employee/<str:uid>/info/",  UserDetailsRetrieveAPIView.as_view(), name="employee-details", ),
    path("all-users/", AllUsersListAPIView.as_view(), name="all-employee-list"),
    path("<str:uid>/",AdminAttendanceDetailAPIView.as_view(),name="admin-attendance-detail",),
]
