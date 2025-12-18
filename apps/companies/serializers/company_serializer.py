from rest_framework import serializers
from ..models import Company
from apps.auths.models import User

class EmployeeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "full_name"]


class CompanySerializer(serializers.ModelSerializer):
    Employees = EmployeeDetailsSerializer(many=True, read_only=True, source='users')
    class Meta:
        model = Company
        fields = ['uid', 'company_name', 'location', 'created_at', 'Employees']
