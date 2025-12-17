from datetime import timedelta
import string
import uuid
import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
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


class UserSecurity(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    def is_reset_token_expired(self):
        if self.reset_token_expires:
            return timezone.now() > self.reset_token_expires
        return True

    def generate_reset_token(self):
        self.reset_token = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=32)
        )
        self.reset_token_expires = timezone.now() + timedelta(minutes=5)
        self.save()
        return self.reset_token

    def __str__(self):
        return f"Security for {self.user.email}"
