import os
import sys
from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    load_dotenv()
    
    environment = os.getenv('DJANGO_ENVIRONMENT', 'development')

    if environment == 'production':
        settings_module = 'config.settings.production'
        print("🚀 Using production settings")
    elif environment == 'development':
        settings_module = 'config.settings.development'
        print("🔧 Using development settings")
    else:
        settings_module = 'config.settings.development'
        print(
            f"⚠️  Unknown environment '{environment}', using development settings")

    # Set the Django settings module directly
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    print(f"📍 Django settings module: {settings_module}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
