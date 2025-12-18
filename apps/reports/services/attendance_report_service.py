from apps.auths.models import User
from ..repositories.attendance_repository import AttendanceRepository
from ..utils.pdf_generator import AttendancePDFGenerator


class AttendanceReportService:
    @staticmethod
    def apply_filters(queryset, filters):
        if filters.get("start_date"):
            queryset = queryset.filter(date__gte=filters["start_date"])

        if filters.get("end_date"):
            queryset = queryset.filter(date__lte=filters["end_date"])

        if filters.get("employee_id"):
            queryset = queryset.filter(user__uid=filters["employee_id"])

        return queryset.order_by("-date", "-created_at")

    @staticmethod
    def generate_company_pdf(company, filters):
        queryset = AttendanceRepository.company_attendance(company)
        queryset = AttendanceReportService.apply_filters(queryset, filters)
        return AttendancePDFGenerator.generate_report(
            attendances=queryset, company=company, filters=filters
        )

    @staticmethod
    def generate_employee_pdf(employee, filters):
        queryset = AttendanceRepository.employee_attendance(employee)
        queryset = AttendanceReportService.apply_filters(queryset, filters)

        return AttendancePDFGenerator.generate_employee_report(
            attendances=queryset, employee=employee, filters=filters
        )

    @staticmethod
    def get_employee(employee_id, company):
        return User.objects.get(uid=employee_id, company=company)
