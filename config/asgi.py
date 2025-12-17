import os
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

load_dotenv()

environment = os.getenv("DJANGO_ENVIRONMENT", "development")
if environment == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

application = get_asgi_application()