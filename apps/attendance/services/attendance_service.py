from ..repositories.attendance_repository import AttendanceRepository

class AttendanceService:

    @staticmethod
    def create_attendance(user, validated_data):
        """
        Rule:
        - Only one attendance per user per day
        - Either NFC or QR must be true
        """
        is_nfc = validated_data.get("is_nfc")
        is_qr = validated_data.get("is_qr")

        if is_nfc == is_qr:
            raise ValueError("Either NFC or QR must be true")

        code = "QR" if is_qr else "NFC"

        attendance = AttendanceRepository.create_attendance(
            user=user,
            code=code,
            **validated_data
        )

        if not attendance:
            raise ValueError("Attendance already submitted for this date")

        return attendance

    @staticmethod
    def list_employee_attendance(user, date=None):
        qs = AttendanceRepository.get_by_user(user)
        return AttendanceRepository.filter_by_date(qs, date)

    @staticmethod
    def list_admin_attendance(date=None):
        qs = AttendanceRepository.get_all()
        return AttendanceRepository.filter_by_date(qs, date)
