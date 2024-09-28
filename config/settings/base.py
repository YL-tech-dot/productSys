"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
"""p.287:
    settings.py c:\projects\mysite\config
        C:\projects]mysite\config\settings\base.py에서 
        .parent가 사용되었으므로 C:\projects\mysite가 될 것이다."""


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'is698z$n$0qxwlihk37e&m=y4es=(g*hrk+d=&4x9rz8(+h-*='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','13.125.89.196']

# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# 미디어 파일 관련 설정
MEDIA_URL= 'media/'
MEDIA_ROOT =  os.path.join(BASE_DIR,'media')

# Application definition

INSTALLED_APPS = [
    'common.apps.CommonConfig', # common 앱을 추가 # CommonConfig 클래스를 추가
    'sales.apps.SalesConfig',  # sales 앱을 추가 # SalesConfig 클래스를 추가
    'django.contrib.admin',
    'django.contrib.auth',  # 장고의 인증 앱 로그인, 로그아웃, 회원가입 등의 기능을 제공
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # templates 디렉터리를 추가
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'
# 'en-us'
TIME_ZONE = 'Asia/Seoul'
# 'UTC'
USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static', # static 디렉터리를 추가
]



MAX_UPLOAD_SIZE = 5242880

ALLOWED_FILE_TYPES=[

    'image/jpeg',
    'image/png',
    'image/gif',
    'image2/jpeg',
    'image2/png',
    'image2/gif',
]

# 로깅설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False, # 만약 True로 설정하면 기존에 설정된 로거들을 사용하지 않게 된다.
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',  # DEBUG=False 인지를 확인하는 필터
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',  # DEBUG=True 인지를 확인하는 필터
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}', # 서버 로그 포맷, 서버 시간과 메시지를 출력
            'style': '{',
        },
        'standard': {# asctime - 현재 시간
            # levelname - 로그의 레벨(debug, info, warning, error, critical)
            # name - 로거명
            # message - 출력 내용
        'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/productSys.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'sales': {
            'handlers': ['console', 'file'],
            'level':'INFO',
        },
    },
}
