from .models import Company
from .serializers.company_serializer import CompanySerializer
from common.pagination.pagination import CustomPagination
from common.api.getApi import BaseListAPIView, BaseRetrieveAPIView

class CompanyListAPIView(BaseListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = CustomPagination
    
class CompanyDetailsAPIView(BaseRetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'uid'
