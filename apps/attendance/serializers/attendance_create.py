from rest_framework import serializers
from ..models import Attendance


class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["uid", "is_nfc", "is_qr", "date"]
