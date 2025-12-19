from django.db import models
from apps.auths.models import User
import uuid

class Attendance(models.Model):
    CODE_CHOICES = (
        ("QR", "QR"),
        ("NFC", "NFC"),
    )

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances")
    is_nfc = models.BooleanField(default=False)
    is_qr = models.BooleanField(default=False)
    code = models.CharField(max_length=3, choices=CODE_CHOICES)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date"]
    def __str__(self):
        return f"{self.user.username} - {self.date}"
