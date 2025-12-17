from apps.attendance.models import Attendance
from django.db import IntegrityError

class AttendanceRepository:

    @staticmethod
    def create_attendance(**data):
        try:
            return Attendance.objects.create(**data)
        except IntegrityError:
            return None

    @staticmethod
    def get_by_user(user):
        return Attendance.objects.filter(user=user)

    @staticmethod
    def get_all():
        return Attendance.objects.select_related("user")

    @staticmethod
    def filter_by_date(queryset, date):
        if date:
            return queryset.filter(date=date)
        return queryset
