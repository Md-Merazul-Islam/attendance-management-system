
import os
from dotenv import load_dotenv
load_dotenv()

ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')
print(f"🚀 Loading Django settings for: {ENVIRONMENT}")

# Import the appropriate settings based on environment
if ENVIRONMENT == 'production':
    try:
        from .production import *
        print("✅ Production settings loaded successfully")
    except ImportError as e:
        print(f"❌ Error loading production settings: {e}")
        print("🔄 Falling back to development settings")
        from .development import *
        print("✅ Development settings loaded as fallback")
elif ENVIRONMENT == 'development':
    try:
        from .development import *
        print("🛠️🔧 Development settings loaded successfully")
    except ImportError as e:
        print(f"❌ Error loading development settings: {e}")
        raise
else:
    print(f"⚠️  Unknown environment '{ENVIRONMENT}', using development settings")
    try:
        from .development import *
        print("✅ Development settings loaded as default")
    except ImportError as e:
        print(f"❌ Error loading development settings: {e}")
        raise

# Debug info
print(f"📍 Django will use environment: {ENVIRONMENT}")
print(f"📍 DEBUG mode: {globals().get('DEBUG', 'Not set')}")
print(f"📍 Database engine: {globals().get('DATABASES', {}).get('default', {}).get('ENGINE', 'Not set')}")