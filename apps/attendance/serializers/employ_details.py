from apps.auths.models import User
from rest_framework import serializers

from apps.attendance.models import Attendance
from apps.companies.models import Company


class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [ "company_name", "location"]


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    company = CompanyDetailsSerializer()
    class Meta:
        model = User
        fields = ["uid", "full_name", "company"]
