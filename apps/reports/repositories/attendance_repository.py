
from apps.attendance.models import Attendance

class AttendanceRepository:

    @staticmethod
    def company_attendance(company):
        return Attendance.objects.filter(
            user__company=company
        ).select_related("user", "user__company")

    @staticmethod
    def employee_attendance(employee):
        return Attendance.objects.filter(
            user=employee
        ).select_related("user", "user__company")
