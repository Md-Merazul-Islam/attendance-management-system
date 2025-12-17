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
from common.utils.permissions import IsEmployee, IsAdministrator
from common.pagination.pagination import CustomPagination
from common.utils.response import success_response, error_response
from common.api.getApi import BaseListAPIView, BaseRetrieveAPIView
from apps.auths.models import User
from rest_framework.permissions import IsAuthenticated


# Employee create attendance
class AttendanceCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

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


# own attendance
class EmployeeAttendanceListAPIView(BaseListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeAttendanceListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Attendance.objects.filter(user=self.request.user)


# Admin all attendance
class AdminAttendanceListAPIView(BaseListAPIView):
    permission_classes = [IsAdministrator]
    queryset = Attendance.objects.all().order_by("-date")
    serializer_class = AdminAttendanceListSerializer
    pagination_class = CustomPagination


# Admin single attendance
class AdminAttendanceDetailAPIView(APIView):
    permission_classes = [IsAdministrator]

    def get(self, request, uid):
        try:
            attendance = self.model.objects.get(uid=uid)
            serializer = self.serializer_class(attendance)
            return success_response(
                "Attendance fetched successfully",
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except self.model.DoesNotExist:
            return error_response(
                "Attendance not found", status=status.HTTP_404_NOT_FOUND
            )


# Admin all employees
class UsersListAPIView(BaseListAPIView):
    permission_classes = [IsAdministrator]
    queryset = User.objects.all()
    serializer_class = EmployeeDetailsSerializer
    pagination_class = CustomPagination


# Admin single employee
class UserDetailsRetrieveAPIView(BaseRetrieveAPIView):
    permission_classes = [IsAdministrator]
    queryset = User.objects.all()
    serializer_class = EmployeeDetailsSerializer
    lookup_field = "uid"
