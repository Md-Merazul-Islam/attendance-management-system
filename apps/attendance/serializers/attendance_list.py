from rest_framework import serializers
from ..models import Attendance

class EmployeeAttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["uid", "is_nfc", "is_qr", "code", "date"]

class AdminAttendanceListSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ["uid", "is_nfc", "is_qr", "date", "employee"]

    def get_employee(self, obj):
        return {
            "uid": obj.user.uid,
            "full_name": obj.user.full_name,
        }
