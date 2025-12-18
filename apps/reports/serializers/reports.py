from rest_framework import serializers

class AttendanceReportSerializer(serializers.Serializer):
    """Serializer for PDF report generation parameters"""
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    employee_id = serializers.UUIDField(required=False)
    
    def validate(self, data):
        """Validate date range"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError(
                    "Start date cannot be greater than end date."
                )
        
        return data