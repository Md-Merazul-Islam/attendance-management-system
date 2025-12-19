from rest_framework import serializers
from ..models import Attendance

class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["uid", "is_nfc", "is_qr", "date"]
        

    # def validate_date(self, value):
    #     """
    #     Validate that the date is today or in the future.
    #     """
    #     if value < date.today():
    #         raise serializers.ValidationError("Attendance date cannot be in the past.")
    #     if value > date.today():
    #         raise serializers.ValidationError("Attendance date cannot be in the future.")
    #     return value