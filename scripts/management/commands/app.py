import os
from pathlib import Path
from django.core.management.base import BaseCommand

MODEL_NAME_PLACEHOLDER = "MyModel"

# Base templates
MODEL_CODE = """from django.db import models

class {model}(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
"""

SERIALIZER_CODE = """from rest_framework import serializers
from ..models import {model}

class {model}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model}
        fields = '__all__'
"""

REPOSITORY_CODE = """class {model}Repository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, pk):
        return self.model.objects.filter(pk=pk).first()
"""

SERVICE_CODE = """from ..repositories import {model}Repository
from ..models import {model}

class {model}Service:
    def __init__(self):
        self.repo = {model}Repository({model})

    def list_items(self):
        return self.repo.get_all()

    def get_item(self, pk):
        return self.repo.get_by_id(pk)
"""


VIEWS_CODE = """from .models import {model}
from .serializers.{model_lower}_serializer import {model}Serializer
from common.api.crud import DynamicModelViewSet
from common.pagination.pagination import CustomPagination

class {model}ViewSet(DynamicModelViewSet):
    queryset = {model}.objects.all()
    serializer_class = {model}Serializer
    pagination_class = CustomPagination

    def __init__(self, *args, **kwargs):
        kwargs['model'] = {model}
        kwargs['serializer_class'] = {model}Serializer
        kwargs['item_name'] = '{model_name}'
        super().__init__(*args, **kwargs)
"""

URLS_CODE = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import {model}ViewSet

router = DefaultRouter()
router.register(r'{model_lower}', {model}ViewSet, basename='{model_lower}')

urlpatterns = [
    path('', include(router.urls)),
]
"""

APPS_CODE = """from django.apps import AppConfig

class {app_cap}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app}'
"""

ADMIN_CODE = """from django.contrib import admin
from .models import {model}

admin.site.register({model})
"""

INIT_CODE = ""
TESTS_CODE = """from django.test import TestCase

# Write your tests here.
"""


# Management Command
class Command(BaseCommand):
    help = "Create a new Django app with full structure: models, serializers, views, services, repositories, permissions"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="Name of the app to create")
        parser.add_argument(
            "--model", type=str, default="MyModel", help="Name of the main model"
        )

    def handle(self, *args, **kwargs):
        app = kwargs["app_name"].lower()
        model = kwargs["model"]
        model_name = model
        base_path = os.path.join("apps", app)

        if os.path.exists(base_path):
            self.stdout.write(self.style.ERROR(f"App '{app}' already exists!"))
            return

        # Create app folders
        os.makedirs(base_path)
        os.makedirs(os.path.join(base_path, "repositories"))
        os.makedirs(os.path.join(base_path, "services"))
        os.makedirs(os.path.join(base_path, "serializers"))

        # Files to create
        files_and_content = {
            "__init__.py": INIT_CODE,
            "models.py": MODEL_CODE.format(model=model),
            # "serializers.py": SERIALIZER_CODE.format(model=model),
            "views.py": VIEWS_CODE.format(model=model, model_name=model_name, model_lower=model.lower()),
            "urls.py": URLS_CODE.format(model=model, model_lower=model.lower()),
            "apps.py": APPS_CODE.format(app=app, app_cap=app.capitalize()),
            "admin.py": ADMIN_CODE.format(model=model),
            "tests.py": TESTS_CODE,
            "repositories/__init__.py": INIT_CODE,
            f"repositories/{model.lower()}_repository.py": REPOSITORY_CODE.format(
                model=model
            ),
            "services/__init__.py": INIT_CODE,
            f"services/{model.lower()}_service.py": SERVICE_CODE.format(model=model),
            "serializers/__init__.py": INIT_CODE,
            f"serializers/{model.lower()}_serializer.py": SERIALIZER_CODE.format(
                model=model
            ),
        }

        # Write files
        for filename, content in files_and_content.items():
            file_path = os.path.join(base_path, filename)
            with open(file_path, "w") as f:
                f.write(content)

        self.add_to_installed_apps(app)
        self.add_to_root_urls(app)

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ App '{app}' with model '{model}' created successfully!"
            )
        )

            

    def add_to_installed_apps(self, app_name: str):
        settings_path = Path("config/settings/base.py")

        if not settings_path.exists():
            self.stdout.write(self.style.WARNING("⚠ base.py not found"))
            return

        content = settings_path.read_text(encoding="utf-8")
        app_entry = f'    "apps.{app_name}",\n'

        if f'"apps.{app_name}"' in content:
            return  # already added

        marker = "# Local apps"
        if marker not in content:
            self.stdout.write(self.style.WARNING("⚠ '# Local apps' marker not found"))
            return

        before, after = content.split(marker, 1)

        # Extract existing local apps block
        local_apps_block = after.split("]", 1)[0]

        updated_local_apps = local_apps_block + app_entry

        updated_content = (
            before
            + marker
            + updated_local_apps
            + "]"
            + after.split("]", 1)[1]
        )

        settings_path.write_text(updated_content, encoding="utf-8")
        print("✅ App added to INSTALLED_APPS")
            
    def add_to_root_urls(self, app_name: str):
        urls_path = Path("config/urls.py")

        if not urls_path.exists():
            self.stdout.write(self.style.WARNING("⚠ urls.py not found"))
            return

        content = urls_path.read_text(encoding="utf-8")

        route_line = f'                path("{app_name}/", include("apps.{app_name}.urls")),\n'

        # Prevent duplicates
        if f'include("apps.{app_name}.urls")' in content:
            return

        api_index = content.find('"api/v1/"')
        if api_index == -1:
            self.stdout.write(self.style.WARNING("⚠ api/v1 block not found"))
            return

        # Find the list [ ... ] that belongs to api/v1
        list_start = content.find("[", api_index)
        list_end = content.find("]", list_start)

        if list_start == -1 or list_end == -1:
            self.stdout.write(self.style.WARNING("⚠ api/v1 include list not found"))
            return

        api_block = content[list_start + 1 : list_end]

        updated_api_block = api_block + route_line

        updated_content = (
            content[: list_start + 1]
            + updated_api_block
            + content[list_end:]
        )

        urls_path.write_text(updated_content, encoding="utf-8")

        self.stdout.write(self.style.SUCCESS("✅ App added to ROOT_URLCONF"))
