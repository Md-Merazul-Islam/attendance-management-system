from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse
from datetime import datetime
from common.utils.permissions import IsAdministrator
from .serializers.reports import AttendanceReportSerializer
from .services.attendance_report_service import AttendanceReportService
from common.utils.response import success_response, error_response


class CompanyAttendancePDFView(APIView):
    """Company Attendance PDF (Admin)"""
    permission_classes = [ IsAdministrator]

    def get(self, request):
        company = request.user.company
        if not company:
            return error_response("Company not found", status=status.HTTP_404_NOT_FOUND)

        serializer = AttendanceReportSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        pdf = AttendanceReportService.generate_company_pdf(
            company=company,
            filters=serializer.validated_data
        )

        filename = f"attendance_report_{datetime.now():%Y%m%d_%H%M%S}.pdf"
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response



class EmployeeAttendancePDFView(APIView):
    """Employee Attendance PDF (Admin)"""
    permission_classes = [ IsAdministrator]

    def get(self, request, employee_id):
        company = request.user.company
        if not company:
            return error_response("Company not found", status=status.HTTP_404_NOT_FOUND)

        serializer = AttendanceReportSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        try:
            employee = AttendanceReportService.get_employee(
                employee_id=employee_id,
                company=company
            )
        except Exception:
            return error_response("Employee not found", status=status.HTTP_404_NOT_FOUND)

        pdf = AttendanceReportService.generate_employee_pdf(
            employee=employee,
            filters=serializer.validated_data
        )

        filename = f"attendance_{employee.full_name.replace(' ', '_')}_{datetime.now():%Y%m%d_%H%M%S}.pdf"
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response



class MyAttendancePDFView(APIView):
    """My Attendance PDF (Employee)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AttendanceReportSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        pdf = AttendanceReportService.generate_employee_pdf(
            employee=request.user,
            filters=serializer.validated_data
        )

        filename = f"my_attendance_{datetime.now():%Y%m%d_%H%M%S}.pdf"
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
