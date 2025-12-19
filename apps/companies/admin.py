from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("uid", "company_name", "location", "created_at")
    search_fields = ("company_name", "location")
    ordering = ("-created_at",)

