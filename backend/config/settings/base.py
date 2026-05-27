# backend/config/settings/base.py
# WHY split into base/development/production?
# Different environments need different settings!
# Development: Debug mode ON, local database
# Production: Debug OFF, real database, HTTPS only

from pathlib import Path
from decouple import config  # Reads from .env file

# ─────────────────────────────────────────────
# BASE DIRECTORY
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# WHY? Django needs to know where the project lives
# Path(__file__) = This file's location
# .parent.parent.parent = Go up 3 folders to root

# ─────────────────────────────────────────────
# SECURITY SETTINGS
# ─────────────────────────────────────────────
SECRET_KEY = config('DJANGO_SECRET_KEY')
# WHY config()? Reads from .env file, NOT hardcoded!
# If someone gets your SECRET_KEY:
# They can forge authentication tokens
# They can access any account
# NEVER hardcode this!

DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
# DEBUG=True shows detailed error pages
# GREAT for development, DANGEROUS in production
# Exposes code structure, database errors to users!

ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', 
                       default='localhost').split(',')
# Which domain names can access this Django app?
# Security: Prevents HTTP Host header attacks

# ─────────────────────────────────────────────
# INSTALLED APPS
# ─────────────────────────────────────────────
DJANGO_APPS = [
    'django.contrib.admin',        # Admin panel (FREE!)
    'django.contrib.auth',         # Authentication system
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session management
    'django.contrib.messages',     # Flash messages
    'django.contrib.staticfiles',  # CSS/JS/Images
]

THIRD_PARTY_APPS = [
    'rest_framework',              # REST API tools
    'rest_framework_simplejwt',    # JWT tokens
    'corsheaders',                 # Allow React to connect
    'channels',                    # WebSockets
]

LOCAL_APPS = [
    'apps.authentication',         # Our auth feature
    'apps.tasks',                  # Our tasks feature
    'apps.habits',                 # Our habits feature
    'apps.gamification',           # XP and levels
    'apps.ai_assistant',           # AI integration
    'apps.notifications',          # Real-time notifications
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# WHY this organization?
# Instantly see: what's Django, what's installed, what's ours
# Professional teams organize it exactly this way

# ─────────────────────────────────────────────
# MIDDLEWARE (Request Processing Pipeline)
# ─────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ↑ Adds security headers (prevents attacks)
    
    'corsheaders.middleware.CorsMiddleware',
    # ↑ Handles CORS for React (MUST be near top!)
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ↑ Manages user sessions
    
    'django.middleware.common.CommonMiddleware',
    # ↑ Various URL normalizations
    
    'django.middleware.csrf.CsrfViewMiddleware',
    # ↑ Prevents Cross-Site Request Forgery attacks
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # ↑ Adds request.user to every request
    
    'django.contrib.messages.middleware.MessageMiddleware',
    # ↑ Flash messages (success/error notifications)
]

# Middleware runs on EVERY request in order:
# Request → Security → CORS → Session → CSRF → Auth → Your View
# Response ← (reverse order)
# Like airport security: multiple checkpoints before boarding

# ─────────────────────────────────────────────
# DATABASE CONFIGURATION
# ─────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # ↑ Use PostgreSQL (not SQLite)
        
        'NAME': config('DB_NAME', default='productivity_rpg'),
        'USER': config('DB_USER', default='rpg_user'),
        'PASSWORD': config('DB_PASSWORD', default='rpg_password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        
        'OPTIONS': {
            'connect_timeout': 10,  # Give up after 10s if can't connect
        },
        
        'CONN_MAX_AGE': 60,
        # ↑ Reuse database connections for 60 seconds
        # Without this: New connection for EVERY request
        # With this: Reuse existing connections (MUCH faster!)
    }
}

# ─────────────────────────────────────────────
# REDIS CONFIGURATION
# ─────────────────────────────────────────────
REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

# Channel Layers (for WebSockets)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    }
}

# ─────────────────────────────────────────────
# REST FRAMEWORK CONFIGURATION
# ─────────────────────────────────────────────
REST_FRAMEWORK = {
    # Default authentication method
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # ↑ Use JWT tokens (not sessions)
        # WHY JWT? React + Django need stateless auth
    ],
    
    # Default permission: Must be logged in
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # ↑ Every endpoint requires login by default
        # Override per-view when needed (login/signup)
    ],
    
    # Pagination (never return unlimited data!)
    'DEFAULT_PAGINATION_CLASS': 
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # ↑ Return max 20 items per page
    # Without pagination: 10,000 tasks = huge response = slow!
    
    # Throttling (rate limiting)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',    # 100 requests per day for strangers
        'user': '1000/day',   # 1000 requests per day for users
    },
    # ↑ Prevents API abuse and DDoS attacks
}

# ─────────────────────────────────────────────
# CORS CONFIGURATION (React ↔ Django)
# ─────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',   # React development server
    'http://127.0.0.1:3000',
]

CORS_ALLOW_CREDENTIALS = True
# ↑ Allow cookies and auth headers cross-origin

# WHY CORS?
# Browser Security Rule: 
# "Only talk to same domain by default"
# React on port 3000 ≠ Django on port 8000
# Without CORS config: Browser BLOCKS the request!
# With CORS config: We explicitly allow it

# ─────────────────────────────────────────────
# CUSTOM USER MODEL (Very Important!)
# ─────────────────────────────────────────────
AUTH_USER_MODEL = 'authentication.User'
# ↑ Use our custom User model, not Django's default
# WHY? Default User model can't be extended easily
# We need: xp, level, avatar, streak fields
# RULE: Always set this BEFORE first migration!
# If you forget: Changing later is very painful!