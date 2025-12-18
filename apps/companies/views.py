from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from common.pagination.pagination import CustomPagination
from common.utils.permissions import IsCompanyAdministrator
from common.utils.response import success_response
from common.api.getApi import BaseListAPIView, BaseRetrieveAPIView
from .models import Company
from .serializers.company_serializer import CompanySerializer


class CompanyListAPIView(BaseListAPIView):
    """
    List all companies accessible to the current company administrator . Each company will include its employees
    """
    permission_classes = [IsCompanyAdministrator]
    serializer_class = CompanySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        admin_user = self.request.user
        # Only show companies assigned to the admin
        return (
            Company.objects.filter(users__uid=admin_user.uid)
            .prefetch_related("users__role")
            .order_by("company_name")
            .distinct()
        )


class CompanyDetailsAPIView(BaseRetrieveAPIView):
    """
    Retrieve details of a company scoped to the admin's assigned company
    """

    permission_classes = [IsCompanyAdministrator]
    serializer_class = CompanySerializer
    lookup_field = "uid"

    def get_queryset(self):
        admin_user = self.request.user
        return Company.objects.filter(users__uid=admin_user.uid).prefetch_related(
            "users__role"
        )


class UpdateCompanyInformation(APIView):
    """
    Update company information (company_name, location). Only accessible by administrators of that company
    """

    permission_classes = [IsCompanyAdministrator]

    def put(self, request, uid):
        admin_user = request.user
        company = get_object_or_404(
            Company.objects.prefetch_related("users__role"),
            uid=uid,
            users__uid=admin_user.uid,
        )

        company.company_name = request.data.get("company_name", company.company_name)
        company.location = request.data.get("location", company.location)
        company.save()

        return success_response(
            "Company information updated successfully",
            {"company": CompanySerializer(company).data},
            status.HTTP_200_OK,
        )
