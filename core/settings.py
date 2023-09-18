"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# Import necessary modules
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

# Load environment variables from a .env file if available
load_dotenv(find_dotenv())

# Define the base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

# List of allowed hostnames for this Django application
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split()

# Define the installed apps for the Django project
INSTALLED_APPS = [
    # Django Core Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your Custom Apps
    'Customers',
    'Items',
    'Orders',
    'Auth',
    
    # Third-party Apps
    'oauth2_provider',
    'rest_framework',
    'rest_framework.authtoken',
]

# Define middleware for handling requests and responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Define the root URL configuration for the project
ROOT_URLCONF = 'core.urls'

# Configure templates for rendering HTML content
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Define the WSGI application for the project
WSGI_APPLICATION = 'core.wsgi.application'

# Database configuration
# DATABASES = {
#     "default": {
#         "ENGINE": os.environ.get("DB_ENGINE"),
#         "NAME": os.environ.get("DB_NAME"),
#         "USER": os.environ.get("DB_USER"),
#         "PASSWORD": os.environ.get("DB_PASSWORD"),
#         "HOST": os.environ.get("DB_HOST"),
#         "PORT": os.environ.get("DB_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) settings
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Define the login URL for the admin panel
LOGIN_URL = '/admin/login/'

# REST framework settings for authentication and permissions
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# OAuth2 provider settings
OAUTH2_PROVIDER = {
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 300,
    "OIDC_ENABLED": True,
    "OIDC_RP_INITIATED_LOGOUT_ENABLED": True,
    "OIDC_RP_INITIATED_LOGOUT_ALWAYS_PROMPT": True,
    "OIDC_RSA_PRIVATE_KEY": os.environ.get("OIDC_RSA_PRIVATE_KEY"),
    "SCOPES": {
        "openid": "OpenID Connect scope",
    },
}
