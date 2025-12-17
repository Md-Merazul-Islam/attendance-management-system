from django.db import models
import uuid

class Company(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    company_name = models.CharField(max_length=255)
    location = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
