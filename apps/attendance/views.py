from rest_framework.views import APIView
from rest_framework import status
from .serializers.attendance_create import AttendanceCreateSerializer
from .serializers.attendance_list import (
    EmployeeAttendanceListSerializer,
    AdminAttendanceListSerializer,
)
from .serializers.employ_details import EmployeeDetailsSerializer
from .models import Attendance
from .services.attendance_service import AttendanceService
from common.utils.permissions import IsAdministrator,IsAdmin
from common.pagination.pagination import CustomPagination
from common.utils.response import success_response, error_response
from common.api.getApi import BaseListAPIView, BaseRetrieveAPIView
from apps.auths.models import User
from rest_framework.permissions import IsAuthenticated
from .utils.attendanceFilter import AttendanceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class AttendanceCreateAPIView(APIView):
    """Create attendance record for authenticated users (Employee or Administrator)."""

    def post(self, request):
        serializer = AttendanceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            attendance = AttendanceService.create_attendance(
                user=request.user, validated_data=serializer.validated_data
            )
            response_serializer = AttendanceCreateSerializer(attendance)
            return success_response(
                "Attendance created successfully",
                response_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return error_response(str(e), status=status.HTTP_400_BAD_REQUEST)


class EmployeeAttendanceListAPIView(BaseListAPIView):
    """List all attendance records for the authenticated employee."""

    serializer_class = EmployeeAttendanceListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AttendanceFilter
    search_fields = ["uid"]

    def get_queryset(self):
        return (
            Attendance.objects.select_related("user")
            .filter(user=self.request.user)
            .order_by("-date")
        )


class EmployeeAttendanceDetailAPIView(BaseRetrieveAPIView):
    """
    Retrieve a single attendance record for the authenticated employee. Employees can only view their own attendance details.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeAttendanceListSerializer
    lookup_field = "uid"

    def get_queryset(self):
        return Attendance.objects.select_related("user").filter(user=self.request.user)


class AdminAttendanceListAPIView(BaseListAPIView):
    """List all attendance records for employees in the Administrator's company."""

    permission_classes = [IsAdministrator]
    serializer_class = AdminAttendanceListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AttendanceFilter
    search_fields = ["uid", "user__full_name"]

    def get_queryset(self):
        # Only show attendance of users in the same company as admin
        admin_company = self.request.user.company
        return (
            Attendance.objects.select_related("user", "user__company")
            .filter(user__company=admin_company)
            .order_by("-date")
        )


class AdminAttendanceDetailAPIView(APIView):
    """
    Allows an Administrator to retrieve details of a single employee only if the employee belongs to the same company.
    """

    permission_classes = [IsAdministrator]

    def get(self, request, uid):
        try:
            admin_company = request.user.company
            attendance = Attendance.objects.select_related("user", "user__company")(
                uid=uid, user__company=admin_company
            )
            serializer = AdminAttendanceListSerializer(attendance)
            return success_response(
                "Attendance fetched successfully",
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Attendance.DoesNotExist:
            return error_response(
                "Attendance not found or not in your company",
                status=status.HTTP_404_NOT_FOUND,
            )


class UserDetailsRetrieveAPIView(BaseRetrieveAPIView):
    """Retrieve details of a single employee."""

    permission_classes = [IsAdministrator]
    serializer_class = EmployeeDetailsSerializer
    queryset = User.objects.all()
    lookup_field = "uid"


class AllUsersListAPIView(BaseListAPIView):
    """Here a super user or main admin can using this api can see all user data"""

    permission_classes = [IsAdmin]
    serializer_class = EmployeeDetailsSerializer
    pagination_class = CustomPagination
    queryset = User.objects.select_related("company", "role").all().order_by("full_name")
