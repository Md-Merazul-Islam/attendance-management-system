from django.urls import path
from .views import CompanyListAPIView, CompanyDetailsAPIView



urlpatterns = [
    path('list/', CompanyListAPIView.as_view(), name='company-list'),
    path('<str:uid>/', CompanyDetailsAPIView.as_view(), name='company-details'),
]
