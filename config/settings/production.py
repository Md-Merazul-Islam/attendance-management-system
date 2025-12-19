import os
from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS = [ "http://206.162.244.143:7773"]


CORS_ALLOWED_ORIGINS = [
    "http://206.162.244.143:7773",
]

CSRF_TRUSTED_ORIGINS = [

    "http://206.162.244.143:7773",
]


# Update DRF settings for production
REST_FRAMEWORK.update(
    {
        "DEFAULT_THROTTLE_CLASSES": [
            "rest_framework.throttling.UserRateThrottle",
            "rest_framework.throttling.AnonRateThrottle",
        ],
        "DEFAULT_THROTTLE_RATES": {
            "user": "1000/hour", 
            "anon": "100/hour", 
        },
        "DEFAULT_RENDERER_CLASSES": [
            "rest_framework.renderers.JSONRenderer",
        ],
    }
)

# Ensure the logs directory exists
log_directory = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(log_directory):
    os.makedirs(log_directory)
    
# Logging configuration for development
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Console handler to log to the console
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        },
        # File handler for saving debug and info logs (in the console)
        "debug_info_file": {
            "class": "logging.FileHandler",
            "filename": "logs/debug_info.log",
            "level": "DEBUG", 
            "formatter": "verbose",
        },
        # File handler for saving warning and higher logs
        "warning_file": {
            "class": "logging.FileHandler",
            "filename": "logs/warning.log",
            "level": "WARNING", 
            "formatter": "verbose",
        },
        # File handler for saving only error logs
        "error_file": {
            "class": "logging.FileHandler",
            "filename": "logs/error.log",
            "level": "ERROR", 
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "debug_info_file", "warning_file", "error_file"],
            "level": "DEBUG",  
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["console", "debug_info_file", "warning_file", "error_file"],
        "level": "DEBUG", 
    },
}


# Security headers
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

print("✅ Production settings loaded")
