from .models import Attendance
from django.contrib import admin

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("uid", "user", "code", "is_nfc", "is_qr", "date")
    search_fields = ("user__full_name", "user__email")
    list_filter = ("code", "is_nfc", "is_qr", "date")
    ordering = ("-date",)