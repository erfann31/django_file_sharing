import os
import sys
from pathlib import Path

# PyInstaller extracts bundled files to a temporary directory. Keep read-only
# application assets there, but save user files beside the executable so they
# are easy to find on every supported operating system.
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
    _executable = Path(sys.executable).resolve()
    if sys.platform == 'darwin':
        # The executable lives inside LocalShare.app/Contents/MacOS. Store
        # files next to the app bundle, rather than inside it.
        _app_bundle = next((parent for parent in _executable.parents if parent.suffix == '.app'), None)
        _default_data_dir = _app_bundle.parent if _app_bundle else _executable.parent
    else:
        _default_data_dir = _executable.parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    _default_data_dir = BASE_DIR

DATA_DIR = Path(os.environ.get('FILE_MANAGER_DATA_DIR', _default_data_dir))
DATA_DIR.mkdir(parents=True, exist_ok=True)

STATIC_URL = '/static/'

SECRET_KEY = 'django-insecure-58*ae*cje4z*im2-&2@v@k+2(mr0(@o$0ve6%2lhnn$arb@%a@'

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'file',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'file_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'file' / 'templates',
        ],
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

WSGI_APPLICATION = 'file_manager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATA_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = BASE_DIR / 'static'
# Uploaded files are placed directly in this visible folder:
#   Windows/Linux: beside LocalShare.exe / LocalShare
#   macOS: beside LocalShare.app
#   Source checkout: beside manage.py
MEDIA_ROOT = DATA_DIR / 'files'
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
MEDIA_URL = '/media/'
