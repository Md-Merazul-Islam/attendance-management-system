from django.urls import path
from .views import CompanyListAPIView, CompanyDetailsAPIView,UpdateCompanyInformation


urlpatterns = [
    path("", CompanyListAPIView.as_view(), name="company-list"),
    path("<str:uid>/", CompanyDetailsAPIView.as_view(), name="company-details"),
    path("<str:uid>/update/", UpdateCompanyInformation.as_view(), name="company-update"),
]
