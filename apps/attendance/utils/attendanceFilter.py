import django_filters
from ..models import Attendance

class AttendanceFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="date", lookup_expr="exact")
    from_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Attendance
        fields = ['date', 'from_date', 'to_date']
