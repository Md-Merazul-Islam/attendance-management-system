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
from .utils.attendanceFilter import AttendanceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AttendanceFilter
    search_fields = ["uid"]

    def get_queryset(self):
        return Attendance.objects.filter(user=self.request.user)


# Admin show is own company all attendance
class AdminAttendanceListAPIView(BaseListAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = AdminAttendanceListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AttendanceFilter
    search_fields = ['uid', 'user__full_name']    

    def get_queryset(self):
        # Only show attendance of users in the same company as admin
        admin_company = self.request.user.company
        return Attendance.objects.filter(user__company=admin_company).order_by('-date')
    
# Admin show is own company  single attendance a particular employee
class AdminAttendanceDetailAPIView(APIView):
    permission_classes = [IsAdministrator]

    def get(self, request, uid):
        try:
            admin_company = request.user.company
            attendance = Attendance.objects.get(uid=uid, user__company=admin_company)
            serializer = AdminAttendanceListSerializer(attendance)
            return success_response(
                "Attendance fetched successfully",
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Attendance.DoesNotExist:
            return error_response(
                "Attendance not found or not in your company",
                status=status.HTTP_404_NOT_FOUND
            )



# Admin show is own company all employees
class UsersListAPIView(BaseListAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = EmployeeDetailsSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["full_name", "email"]

    def get_queryset(self):
        admin_company = self.request.user.company
        if not admin_company:
            return User.objects.none()
        return User.objects.filter(company=admin_company, role__role_name="Employee")



# Admin show is own company  single employee
class UserDetailsRetrieveAPIView(BaseRetrieveAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = EmployeeDetailsSerializer
    lookup_field = "uid"

    def get_queryset(self):
        admin_company = self.request.user.company
        if not admin_company:
            return User.objects.none()
        return User.objects.filter(company=admin_company, role__role_name="Employee")



#here the all user records will be fetched
class AllUsersListAPIView(BaseListAPIView):
    permission_classes = [IsAdministrator]
    queryset = User.objects.all()
    serializer_class = EmployeeDetailsSerializer
    pagination_class = CustomPagination