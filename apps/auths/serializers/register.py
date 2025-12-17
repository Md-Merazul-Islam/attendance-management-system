
from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    ROLE_CHOICES = ["employee", "administrator"]

    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    company_uid = serializers.UUIDField(required=False)    # Employee fields
    company_name = serializers.CharField(required=False)    # Admin fields
    location = serializers.CharField(required=False)

    def validate(self, data):
        role = data.get("role")
        if role == "Employee":
            if not data.get("company_uid"):
                raise serializers.ValidationError({"company_uid": "This field is required for Employee"})
        elif role == "Administrator":
            if not data.get("company_name"):
                raise serializers.ValidationError({"company_name": "This field is required for Administrator"})
            if not data.get("location"):
                raise serializers.ValidationError({"location": "This field is required for Administrator"})
        else:
            raise serializers.ValidationError({"role": "Invalid role"})
        return data
