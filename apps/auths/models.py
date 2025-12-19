import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.companies.models import Company
from .utils.customUser import CustomUserManager


class Role(models.Model):
    role_name = models.CharField(max_length=20)

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    location = models.TextField(blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    username = None
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]
    @property
    def id(self):
        return self.uid
    
    @id.setter
    def id(self, value):
        self.uid = value
    def __str__(self):
        return f"{self.full_name} - {self.email} - {self.date_joined}"

